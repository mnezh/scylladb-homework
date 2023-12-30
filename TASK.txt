Python ScyllaDB Coding Task Description: 

You are going to simulate client stress on the ScyllaDB database and analyze the stress results.

The exercise consists of two parts: 

    Deploying a single node ScyllaDB cluster on docker and getting to know the cassandra-stress command (you can read a bit about cassandra-stress here, but it’s not mandatory for this task) .

    Coding a small program (analysis and runner program) that will run several threads of cassandra-stress and analyze their results.

Deploying single node scylla cluster on docker (~10-15 minutes)

    Follow the steps here to deploy a single node scylla cluster (you can stop after the "Run nodetool utility" step).

    Exercise the running the cassandra-stress command by using the command:
    " docker exec some-scylla cassandra-stress write duration=10s -rate threads=10 -node node_ip_from_nodetool_output"

    Understand the cassandra-stress results output.
    When cassandra-stress output completes it provides a results summary that looks like this:

Results:

﻿Op rate : 2,387 op/s [WRITE: 2,387 op/s]
Partition rate : 2,387 pk/s [WRITE: 2,387 pk/s]
Row rate : 2,387 row/s [WRITE: 2,387 row/s]
Latency mean : 4.0 ms [WRITE: 4.0 ms]
Latency median : 2.8 ms [WRITE: 2.8 ms]
Latency 95th percentile : 10.5 ms [WRITE: 10.5 ms]
Latency 99th percentile : 19.9 ms [WRITE: 19.9 ms]
Latency 99.9th percentile : 69.5 ms [WRITE: 69.5 ms]
Latency max : 115.7 ms [WRITE: 115.7 ms]
Total partitions : 7,292 [WRITE: 7,292]
Total errors : 0 [WRITE: 0]
Total GC count : 0
Total GC memory : 0.000 KiB
Total GC time : 0.0 seconds
Avg GC time : NaN ms
StdDev GC time : 0.0 ms
Total operation time : 00:00:03

END

Analysis and runner program

The Analysis program will run concurrently N cassandra-stress commands while each one of them will run in a separate thread.
The analysis program should parse the results summary of each of the cassandra-stress threads and print the aggregated summary for all of the threads.

Requirements:

    Number of concurrent stress commands to run will be received as a command line argument.

    Each stress command runtime duration may be different.

    The program should print an aggregated summary with the details below.

        Number of stress processes that ran.

        Start/end time of each stress process and its duration

        Calculated aggregation of "Op rate" (sum).

        Calculated average of "Latency mean" (average).

        Calculated average of "Latency 99th percentile" (average).

        Standard deviation calculation of all "Latency max" results.

Guidelines:

    Write object-oriented code

    Use argparse to parse command line arguments

    For statistics calculations use only standard lib functions

    We do not want you to invest too much time and effort on this assignment, so it doesn't need to be a "production grade" program, but we do want to know how long it took you to do it.

    Bonus: production grade code

Submission:

Please provide your completed home task as a GitHub repository or a compressed file (e.g., ZIP) containing the code, any necessary configuration files, and a README how to  to run the code.
Evaluation Criteria:

Your home task will be evaluated based on the following criteria:

    Code Quality: Is your test code well-organized, readable, and maintainable?

    Validation of the output: Does the code output is according to the requirements?

    Documentation: Is your README comprehensive and clear, providing instructions for setting up and running the program.