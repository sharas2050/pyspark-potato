# pyspark-potato
Pyspark project for telecom. Showing data engineering skills with python, spark.
Also includes 2 examples of algorithm understanding: discrete-event simulation (DES) and Directions Reduction
## Pre-requisites ##

* IntelliJ IDEA
* Python 3.9
* Spark 3.2.4
* Windows binaries for Hadoop versions

## Running application
### Application covers 3 use cases:
#### Path Reduction_Case1
function `reducePath` which will take a list of strings and returns a list of strings with the needless paths removed (W<->E or S<->N side by side).

```shell
python.exe reducePath.py --path NORTH SOUTH NORTH
```

#### Grocery Store Simulation_Case2
function `computecheckouttime` which will take an array of positive integers representing the customers and returns an integer which would be the total time required to check out for all the customers.
```shell
python.exe computecheckouttime.py --customers 5 3 4 --counters 1
```
### Telecom Site and Cells Case_3
Data engineering task solved by using pyspark. Application creates data sets for cells and frequency bands for each site.
It exposes some intermediate data sets also used for data ingestion, preparation etc.

There is 2 examples of application running locally and on HDFS.

```shell
python.exe local.py
```
```shell
python.exe hdfs.py ${OUTPUT_DIR}
python.exe hdfs.py C:\pyspark\out
```
