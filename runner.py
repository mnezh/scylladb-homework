#!/usr/bin/env python3
import argparse
import logging
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from statistics import stdev


def main():
    args = parse_args()
    setup_log(args.log_level)
    runner = get_runner(args)
    runner.run()
    runner.report()


@dataclass
class RunResult:
    start: datetime
    end: datetime
    duration: str
    op_rate: int
    latency_mean: float
    latency_99: float
    latency_max: float

    @property
    def actual_duration(self):
        return (self.end - self.start).total_seconds()


class Worker:
    def __init__(self, scylla_name: str, node_ip: str, duration: str) -> None:
        self.log = logging.getLogger("worker")
        self.scylla_name = scylla_name
        self.node_ip = node_ip
        self.duration = duration
        self.op_rate = 0
        self.latency_mean = 0.0
        self.latency_99 = 0.0
        self.latency_max = 0.0

    def run(self) -> RunResult:
        self.log.debug(f"Starting worker {self.duration}")
        start = datetime.now()
        p = subprocess.run(
            [
                "docker",
                "exec",
                self.scylla_name,
                "cassandra-stress",
                "write",
                f"duration={self.duration}",
                "-rate",
                "threads=10",  # probably should be 1?
                "-node",
                self.node_ip,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        end = datetime.now()
        for line in p.stderr.decode().split("\n"):
            self.log.warning(line)
        self.log.debug(f"Ending worker {self.duration=}")
        return self.result(start, end, p.stdout.decode())

    def result(self, start: datetime, end: datetime, stdout: str) -> RunResult:
        res = re.findall(r"Results:\n((.|\n)*)\n\nEND", stdout, re.MULTILINE)[0][0]
        return RunResult(
            start=start,
            end=end,
            duration=self.duration,
            op_rate=self.get_int(res, "Op rate"),
            latency_mean=self.get_float(res, "Latency mean"),
            latency_99=self.get_float(res, "Latency 99th percentile"),
            latency_max=self.get_float(res, "Latency max"),
        )

    def get_int(self, res: str, name: str) -> int:
        return int(re.match(name + r"\s+:\s+((\d|,)+)", res)[1].replace(",", ""))

    def get_float(self, res: str, name: str) -> float:
        return float(re.findall(name + r"\s+:\s+((\d|\.)+)", res)[0][0])


class Runner:
    def __init__(self, scylla_name: str, command_durations: list[str]):
        self.scylla_name = scylla_name
        self.command_durations = command_durations
        self.log = logging.getLogger("runner")
        self.results: list[RunResult] = []
        self.fetch_ip()

    def fetch_ip(self):
        stdout = subprocess.run(
            ["docker", "exec", "-it", self.scylla_name, "nodetool", "status"],
            stdout=subprocess.PIPE,
            check=False,
        ).stdout.decode()
        self.node_ip = re.findall(r"UN\s+((\d|\.)*)", stdout)[0][0]

    def run(self):
        self.log.info(
            f"Going to run {len(self.command_durations)} commands with "
            f"durations {self.command_durations}"
        )
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(Worker(self.scylla_name, self.node_ip, duration).run)
                for duration in self.command_durations
            ]
            self.results = [future.result() for future in futures]

    def op_rate_aggregation(self) -> int:
        return sum([res.op_rate for res in self.results])

    def average_latency_mean(self) -> float:
        if self.results:
            return sum([res.latency_mean for res in self.results]) / len(self.results)
        return 0.0

    def average_latency_99(self) -> float:
        if self.results:
            return sum([res.latency_99 for res in self.results]) / len(self.results)
        return 0.0

    def stddev_latency_max(self) -> float:
        return stdev([res.latency_max for res in self.results])

    def report(self):
        print("\nReport:\n")
        print(f"Number of stress processes that ran: {len(self.results)}")
        print("Start/end time of each stress process and its duration:")
        print(
            "  | start                      | end                        "
            "| duration | run time   |"
        )
        for res in self.results:
            print(
                "  | {} | {} | {:>9}| {:>9}s |".format(
                    res.start.isoformat(),
                    res.end.isoformat(),
                    res.duration,
                    res.actual_duration,
                )
            )
        print('Calculated aggregation of "Op rate" (sum):', self.op_rate_aggregation())
        print('Calculated average of "Latency mean": ', self.average_latency_mean())
        print(
            'Calculated average of "Latency 99th percentile" (average):',
            self.average_latency_99(),
        )
        print(
            'Standard deviation calculation of all "Latency max" results:',
            self.stddev_latency_max(),
        )


def setup_log(log_level: str):
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s [%(name)s:%(threadName)s] %(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )


def parse_args() -> Runner:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", default="info", help="log level")
    parser.add_argument(
        "-n", type=int, default=0, help="Number of concurrent stress commands"
    )
    parser.add_argument(
        "-s", "--scylla-name", required=True, help="Name of ScyllaDB container"
    )
    parser.add_argument(
        "duration", nargs="*", help="List of stress command durations", default=["10s"]
    )
    return parser.parse_args()


def get_runner(args: argparse.Namespace) -> Runner:
    if args.n == 0:
        return Runner(args.scylla_name, args.duration)
    durations = []
    while len(durations) < args.n:
        durations += args.duration
    return Runner(args.scylla_name, durations[0 : args.n])


if __name__ == "__main__":
    main()
