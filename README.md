# Docker of Hive, Presto and Hadoop HDFS

The idea of this repo is to provide some simple step by step guide to set up an isolated test/dev version Hive & PrestoDB locally and start playing around with it :-).
This set up is totally NOT recommended for production workloads.

## Set up Hive & PrestoDB locally (isolated)
Because our purpose is just to experiment, to accelerate the set up we could use docker images (to be accurate, docker-compose).
First of all we need to clone this repo:
```
$ git clone git@github.com:dinhnhatbang/hive-presto-docker.git
$ cd hive-presto-tutorial
$ make
```
The first step is to build the docker images and start the cluster based on those images.
To do that we'll execute the following command **from the root of this project**(*):
```
$ docker-compose up -d
```
After that we will create initial tables of hive metastore:
```
$ docker-compose exec hive-server bash
```
Run script for create initial tables of MySQL:
```
# /opt/hive/bin/schematool -dbType mysql -initSchema
```
Exit and restart again of **hive-metastore**
```
$ docker-compose up -d hive-metastore
```
Checking again of **docker-compose** to make sure all services are running:
```
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                    PORTS                                          NAMES
bfbaf06b3e47        hadoop/datanode     "/entrypoint.sh /run…"   22 minutes ago      Up 22 minutes (healthy)   0.0.0.0:9864->9864/tcp                         datanode
e9843e403a81        hadoop/namenode     "/entrypoint.sh /run…"   22 minutes ago      Up 22 minutes (healthy)   0.0.0.0:9870->9870/tcp                         namenode
49e8ad8b0be7        hive                "entrypoint.sh /bin/…"   22 minutes ago      Up 22 minutes             0.0.0.0:10000->10000/tcp, 10002/tcp            hive-server
93ebf04c01f7        hive                "entrypoint.sh /opt/…"   22 minutes ago      Up 20 minutes             10000/tcp, 0.0.0.0:9083->9083/tcp, 10002/tcp   hive-metastore
7cc7389039be        mysql:5.7.25        "docker-entrypoint.s…"   22 minutes ago      Up 22 minutes             0.0.0.0:3306->3306/tcp, 33060/tcp              mysql
5a5d4d2cd85f        prestodb            "./bin/launcher run"     22 minutes ago      Up 22 minutes             0.0.0.0:8080->8080/tcp                         presto-coordinator
```
(*) We are assuming that you have docker installed and configured, if not take a look to this [guide](https://docs.docker.com/install/overview/)

## Getting some data to analyze
In our example we'll be analyzing the following file [temp-data.csv](temp-data.csv), here you can see a sample:
```
2018-01-01T01:00:00,52
2018-01-01T02:00:00,50
2018-01-01T03:00:00,48
2018-01-01T04:00:00,48
2018-01-01T05:00:00,45
...
```
That file contains the temperature measured every hour from a weather station for all 2018.

## Analyzing data
The first step to use is to create the table with the data to analyze, we are going to use Hive for that, execute the following command to open shell into a cluster machine:
```
docker-compose exec hive-server bash
```
Copy the file to HDFS:
```
# hdfs dfs -mkdir /data
# hdfs dfs -put /data/temp-data.csv /data/temp-data.csv
```
Connect the JDBC driver:
```
# /opt/hive/bin/beeline -u jdbc:hive2://localhost:10000
```
Finally create the table from the data in the file:
```
> CREATE EXTERNAL TABLE horlytemp(time STRING, temp INT) COMMENT 'temperature from csv file' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE location '/data';
```
We can check if the data is accessible doing:
```
> select * from horlytemp;
```
We should see the list of temperatures.

### Querying in presto

Download presto client from: https://prestodb.io/docs/current/installation/cli.html
Rename it to just "presto" and make it executable as described on that page.

Now let's execute the presto client:
```
./presto --server localhost:8080 --catalog hive --schema default
```

Finally, from that shell we can query that table, for instance:
```
# select * from horlytemp where temp > 80;
```
We should see something like: 
```
       time         | temp
---------------------+------
 2018-05-15T17:00:00 |   81
 2018-06-17T10:00:00 |   81
 2018-06-17T11:00:00 |   84
 2018-06-17T12:00:00 |   86
 2018-06-17T13:00:00 |   86
```

### Clean up
Stop the docker containers and remove volumes by doing:
```
$ docker-compose down
$ docker volume rm hive-presto-docker_datanode hive-presto-docker_namenode
```

## References
- Hive-presto docker compose: https://github.com/big-data-europe/docker-hive
- Hadoop docker compose: https://github.com/big-data-europe/docker-hadoop
- Presto docker: https://github.com/IBM/docker-prestodb 
- HIVE-PRESTODB TUTORIAL: https://github.com/jordicenzano/hive-presto-tutorial
- A twitter crawler in Python: https://github.com/bianjiang/tweetf0rm
