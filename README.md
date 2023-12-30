# What's there
A homework for ScyllaDB based on [TASK.txt](TASK.txt)

* [runner.py](runner.py) - runs parallel `cassandra-stress` for scyllaDB in docker container and generates report, doesn't need any extra package
* [Makefile](Makefile) - automates tasks (scylla container, python linter/formatting, venv dev setup)
* [requirements.txt](requirements.txt) - dev requirements for python venv
* [pyproject.toml] - configuration for `ruff` linter/formatter

# Setup
Start scyllaDB:

```shell
$ make scylla-run
```

Check that is is alive:
```shell
$ make scylla-status
```

Optionally execute stress test command to get a sample `cassandra-stress` output:
```shell
$ make scylla-stress
```

If you're going to contribute, create venv with `ruff` installed:

```shell
$ make setup
```

Check or autofix your code after making changes:

```shell
$ make style
$ make format
```

# Run the tool

```shell
$ ./runner.py --help
usage: runner.py [-h] [-l LOG_LEVEL] [-n N] -s SCYLLA_NAME [duration ...]

positional arguments:
  duration              List of stress command durations

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        log level
  -n N                  Number of concurrent stress commands
  -s SCYLLA_NAME, --scylla-name SCYLLA_NAME
                        Name of ScyllaDB container
```

Example 1: run 7 parallel tests with durations '10s', '15s', '7s', '10s', '15s', '7s', '10s'

```shell
$ ./runner.py -s some-scylla -n 7 10s 15s 7s
```

Example 2: run 3 parallel tests with durations '10s', '15s', '7s'

```shell
$ ./runner.py -s some-scylla 10s 15s 7s
```

Example 3: run tests with debug log:
```shell
$./runner.py -l DEBUG -s some-scylla -n 7 10s 15s 7s
```

# Sample output

```shell
$ ./runner.py -l DEBUG -s some-scylla -n 7 10s 15s 7s
2023-12-30 20:45:52,020 [runner:MainThread] INFO Going to run 7 commands with durations ['10s', '15s', '7s', '10s', '15s', '7s', '10s']
2023-12-30 20:45:52,021 [worker:ThreadPoolExecutor-0_0] DEBUG Starting worker self.duration='10s'
2023-12-30 20:45:52,021 [worker:ThreadPoolExecutor-0_1] DEBUG Starting worker self.duration='15s'
2023-12-30 20:45:52,022 [worker:ThreadPoolExecutor-0_2] DEBUG Starting worker self.duration='7s'
2023-12-30 20:45:52,022 [worker:ThreadPoolExecutor-0_3] DEBUG Starting worker self.duration='10s'
2023-12-30 20:45:52,024 [worker:ThreadPoolExecutor-0_4] DEBUG Starting worker self.duration='15s'
2023-12-30 20:45:52,025 [worker:ThreadPoolExecutor-0_5] DEBUG Starting worker self.duration='7s'
2023-12-30 20:45:52,029 [worker:ThreadPoolExecutor-0_6] DEBUG Starting worker self.duration='10s'
2023-12-30 20:46:14,269 [worker:ThreadPoolExecutor-0_2] WARNING WARN  19:45:53,700 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:14,269 [worker:ThreadPoolExecutor-0_2] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:14,269 [worker:ThreadPoolExecutor-0_2] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:14,269 [worker:ThreadPoolExecutor-0_2] WARNING 
2023-12-30 20:46:14,269 [worker:ThreadPoolExecutor-0_2] DEBUG Ending worker self.duration='7s'
2023-12-30 20:46:14,297 [worker:ThreadPoolExecutor-0_5] WARNING WARN  19:45:53,714 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:14,297 [worker:ThreadPoolExecutor-0_5] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:14,297 [worker:ThreadPoolExecutor-0_5] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:14,297 [worker:ThreadPoolExecutor-0_5] WARNING 
2023-12-30 20:46:14,297 [worker:ThreadPoolExecutor-0_5] DEBUG Ending worker self.duration='7s'
2023-12-30 20:46:17,151 [worker:ThreadPoolExecutor-0_0] WARNING WARN  19:45:53,663 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:17,151 [worker:ThreadPoolExecutor-0_0] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,151 [worker:ThreadPoolExecutor-0_0] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,151 [worker:ThreadPoolExecutor-0_0] WARNING 
2023-12-30 20:46:17,151 [worker:ThreadPoolExecutor-0_0] DEBUG Ending worker self.duration='10s'
2023-12-30 20:46:17,198 [worker:ThreadPoolExecutor-0_6] WARNING WARN  19:45:53,674 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:17,198 [worker:ThreadPoolExecutor-0_6] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,198 [worker:ThreadPoolExecutor-0_6] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,198 [worker:ThreadPoolExecutor-0_6] WARNING 
2023-12-30 20:46:17,198 [worker:ThreadPoolExecutor-0_6] DEBUG Ending worker self.duration='10s'
2023-12-30 20:46:17,251 [worker:ThreadPoolExecutor-0_3] WARNING WARN  19:45:53,642 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:17,251 [worker:ThreadPoolExecutor-0_3] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,251 [worker:ThreadPoolExecutor-0_3] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:17,251 [worker:ThreadPoolExecutor-0_3] WARNING 
2023-12-30 20:46:17,251 [worker:ThreadPoolExecutor-0_3] DEBUG Ending worker self.duration='10s'
2023-12-30 20:46:22,184 [worker:ThreadPoolExecutor-0_1] WARNING WARN  19:45:53,577 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:22,184 [worker:ThreadPoolExecutor-0_1] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:22,184 [worker:ThreadPoolExecutor-0_1] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:22,184 [worker:ThreadPoolExecutor-0_1] WARNING 
2023-12-30 20:46:22,184 [worker:ThreadPoolExecutor-0_1] DEBUG Ending worker self.duration='15s'
2023-12-30 20:46:22,275 [worker:ThreadPoolExecutor-0_4] WARNING WARN  19:45:53,683 Query '[0 bound values] CREATE KEYSPACE IF NOT EXISTS "keyspace1" WITH replication = {'class': 'org.apache.cassandra.locator.SimpleStrategy', 'replication_factor' : '1'} AND durable_writes = true;' generated server side warning(s): Using Replication Factor replication_factor=1 lower than the minimum_replication_factor_warn_threshold=3 is not recommended.
2023-12-30 20:46:22,275 [worker:ThreadPoolExecutor-0_4] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:22,275 [worker:ThreadPoolExecutor-0_4] WARNING Failed to connect over JMX; not collecting these stats
2023-12-30 20:46:22,275 [worker:ThreadPoolExecutor-0_4] WARNING 
2023-12-30 20:46:22,275 [worker:ThreadPoolExecutor-0_4] DEBUG Ending worker self.duration='15s'

Report:

Number of stress processes that ran: 7
Start/end time of each stress process and its duration:
  | start                      | end                        | duration | run time   |
  | 2023-12-30T20:45:52.021295 | 2023-12-30T20:46:17.151471 |       10s| 25.130176s |
  | 2023-12-30T20:45:52.021468 | 2023-12-30T20:46:22.184036 |       15s| 30.162568s |
  | 2023-12-30T20:45:52.022772 | 2023-12-30T20:46:14.269076 |        7s| 22.246304s |
  | 2023-12-30T20:45:52.022939 | 2023-12-30T20:46:17.251211 |       10s| 25.228272s |
  | 2023-12-30T20:45:52.025047 | 2023-12-30T20:46:22.275213 |       15s| 30.250166s |
  | 2023-12-30T20:45:52.025307 | 2023-12-30T20:46:14.297879 |        7s| 22.272572s |
  | 2023-12-30T20:45:52.029458 | 2023-12-30T20:46:17.198032 |       10s| 25.168574s |
Calculated aggregation of "Op rate" (sum): 61809
Calculated average of "Latency mean":  1.1571428571428573
Calculated average of "Latency 99th percentile" (average): 2.585714285714286
Standard deviation calculation of all "Latency max" results: 2.7878990211951633
```