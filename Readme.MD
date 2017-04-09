Process flow:

The premise of this application is to consume the incoming streaming data of feeds through a mix of technology.
a. Kafka - fault tolerant method of consuming feeds or messages.We can use a series of sinks/source to finally deliver the message to backend
b. python - used for processing of incoming feed using skilearn, pandas, numpy where datamining happens almost realtime
c. avro - used for serialization of incoming and outgoing formats to ensure easy modifications/updates going forward

Example flow:

--> Product feed -->Queue-->Kafka Consumer-->Python Productprocessor-->Kafka Producer --> Python ProductAnalyzer -->Kafka Connect-->Cassandra

In future we may decide to move away from python and probably integrate with a Apache flink framework when we can easily change the python processing framework using Apache flink without disturbing the entire cassandra, kafka and avro framework usage.


Steps to execute:

1. Install a few packages as given below in python.
```bash
pip install avro
pip install logging
pip install numpy
pip install pandas
pip install scilearn
pip install kafka
pip install cassandra-driver

2. Assuming kafka/zookeeper is already there, you need to proceed with kafka-topics.sh --create command. If not follow the steps here.

a. In case its standalone, just configure the localhost:2181 property in zookeeper.properties file in kafka config folder.
    i. If you want to simulate multi server setup for zookeeper cluster then
    you can copy zookeeper package in three folders e.g. instance 1, instance 2, instance 3. In each of these, zoo.cfg files update clientport=2181, 2182 and 2183 etc as required.
    ii. update the data folder to /data/zk1/, /data/zk2/, /data/zk3/ or whichever path but different from each.
    iii. add following property in all the three zoo.cfg file
    ```bash
    server.1=localhost:2888:3888
    server.2=localhost:2889:3890
    server.3=localhost:2890:3890
    ```
    Here ensure server.1 i.e. 1 is same as the server identifier which you will configure in next step within myid file of the data folder.
    iv. execute following command in each of these folders and have 1,2,3 as id in the myid file
    ```bash
    touch myid
    vi my id
    1 # or 2 or 3 depending on zk1, zk2, zk3 folder
    :wq
    ```
    The above is important since all the feeds/data is going to be saved in the folder under /data/zk1/ and uses the identifer used for server in managing the partition tolerance/replication across servers.
    v. Goto kafka config folder and open server.properties file. Here update zookeeper.connect to localhost:2181
    vi. Repeat the above by creating copies of server.properties as server-2.properties and server-3.properties. Update the zookeeper.connect to respective zookeeper url i.e. localhost:2181 etc
    Also ensure brokder id used for each broker i.e. instance of server properties file is unique and configured as in zookeeper properties in section#a above.


    ```bash
    brokder.id =1
    ```


    Note that you can provide multiple connection urls for zookeeper to ensure high availability , partition tolerance.
    E.g. to keep simple given localhost below but this could be your IPs of servers in the node which perform zookeeper's cluster management.
    ```bash
    zookeeper.connect = localhost:2181,localhost:2182,localhost:2183
    ```
    It is a good practice to store all the log.dirs and datadir in kafka broker and zookeeper on common mounts and providing execute i.e. chmod 755 access.

b. Execute the create queue command. Important to note what partition you would use. Partition of 1 with replication of 2 or 3 is better than multiple partition in most cases since sequence(called offsets) generated across those topics we would need to be unique across platform. Again, this is dependant on usecases.
```bash
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 2 --topic  bespoke.avro.product
```
When above is done, we actually are distributing across 3 servers. Offsets are critical for time based data hence we need to use this wisely.
E.g. Only when we have more than 4 nodes, its preferred to have replication factor of 2. I prefer a 2n+1 formula to find my repl factor. Indicative number given below:

        nodes	repl factor
        3	    1
        4	    1
        5   	2
        6	    2
        8	    3
        10	    4

Use multiple partition when we really see no issue in sequence or offset counts impacting processing logic and we need sequential processing power.

c. Producers in this program have been categorized through stub. I have simulated producer through generated load pushed from generateload.
Key properties to configure are broker-list which can be localhost:9092,localhost:9093,localhost:9094. If we have multiple servers you can give the IP details.

d. Review and check ISR and leader IP etc using

```bash
kafka-topics.sh --describe --zookeeper localhost:2181 --topic bespoke.avro.product
```



