# FLiP-Pi-BreakoutGarden

## FLiP-Py



### Gear / Hardware

* Raspberry Pi 3 Model B Rev 1.2, Bullseye Raspian, armv71
* Pimoroni Breakout Garden Hat
* 1.12" Mono OLED Breakout 128x128 White/Black Screen
* BME680 Air Quality, Temperature, Pressure, Humidity Sensor
* LWM303D 6D0F Motion Sensor (X, Y, Z Axes)
* BH1745 Luminance and Color Sensor
* LTR-559 Light and Proximity Sensor 0.01 lux to 64,000 lux
* VL53L1X Time of Flight (TOF) Sensor

![Device](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorsboard.jpg)

### Software / Libraries

* Python 3.9 
* Pulsar Python Client 2.10 (avro) pip3 install pulsar-client[avro]
* Python Breakout Garden
* Python PSUTIL https://pypi.org/project/psutil/
* Python LUMA OLED pip3 install --upgrade luma.oled
* Libraries sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y

![Architecture](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/pisensors.png?raw=true)

### StreamOps

````
bin/pulsar-admin topics create "persistent://public/default/pi-sensors"

````

### Device Running

````
VL53L0X_GetDeviceInfo:
Device Name : VL53L1 cut1.1
Device Type : VL53L1
Device ID : 
ProductRevisionMajor : 1
ProductRevisionMinor : 15
{'_required_default': False, '_default': None, '_required': False, 'uuid': 'snr_20220323200032', 'ipaddress': '192.168.1.229', 'cputempf': 99, 'runtime': 154, 'host': 'piups', 'hostname': 'piups', 'macaddress': 'b8:27:eb:4a:4b:61', 'endtime': '1648065632.645613', 'te': '154.00473523139954', 'cpu': 0.0, 'diskusage': '3895.3 MB', 'memory': 21.5, 'rowid': '20220323200032_6a66f9ea-1273-4e5d-b150-9300f6272482', 'systemtime': '03/23/2022 16:00:33', 'ts': 1648065633, 'starttime': '03/23/2022 15:57:58', 'BH1745_red': 112.2, 'BH1745_green': 82.0, 'BH1745_blue': 63.0, 'BH1745_clear': 110.0, 'VL53L1X_distance_in_mm': -1185.0, 'ltr559_lux': 6.65, 'ltr559_prox': 0.0, 'bme680_tempc': 23.6, 'bme680_tempf': 74.48, 'bme680_pressure': 1017.48, 'bme680_humidity': 33.931, 'lsm303d_accelerometer': '-00.08g : -01.00g : +00.01g', 'lsm303d_magnetometer': '+00.06 : +00.30 : +00.07'}
VL53L1X Start Ranging Address 0x29

````

### Consumer

````

bin/pulsar-client consume "persistent://public/default/pi-sensors" -s "pisnsrgrdnrdr" -n 0


````

### ** SQL Consumers **

#### Pulsar SQL / Presto/Trino

````

desc pulsar."public/default"."pi-sensors";

         Column         |   Type    | Extra |                                   Comment                                   
------------------------+-----------+-------+-----------------------------------------------------------------------------
 uuid                   | varchar   |       | ["null","string"]                                                           
 ipaddress              | varchar   |       | ["null","string"]                                                           
 cputempf               | integer   |       | ["null","int"]                                                              
 runtime                | integer   |       | ["null","int"]                                                              
 host                   | varchar   |       | ["null","string"]                                                           
 hostname               | varchar   |       | ["null","string"]                                                           
 macaddress             | varchar   |       | ["null","string"]                                                           
 endtime                | varchar   |       | ["null","string"]                                                           
 te                     | varchar   |       | ["null","string"]                                                           
 cpu                    | real      |       | ["null","float"]                                                            
 diskusage              | varchar   |       | ["null","string"]                                                           
 memory                 | real      |       | ["null","float"]                                                            
 rowid                  | varchar   |       | ["null","string"]                                                           
 systemtime             | varchar   |       | ["null","string"]                                                           
 ts                     | integer   |       | ["null","int"]                                                              
 starttime              | varchar   |       | ["null","string"]                                                           
 bh1745_red             | real      |       | ["null","float"]                                                            
 bh1745_green           | real      |       | ["null","float"]                                                            
 bh1745_blue            | real      |       | ["null","float"]                                                            
 bh1745_clear           | real      |       | ["null","float"]                                                            
 vl53l1x_distance_in_mm | real      |       | ["null","float"]                                                            
 ltr559_lux             | real      |       | ["null","float"]                                                            
 ltr559_prox            | real      |       | ["null","float"]                                                            
 bme680_tempc           | real      |       | ["null","float"]                                                            
 bme680_tempf           | real      |       | ["null","float"]                                                            
 bme680_pressure        | real      |       | ["null","float"]                                                            
 bme680_humidity        | real      |       | ["null","float"]                                                            
 lsm303d_accelerometer  | varchar   |       | ["null","string"]                                                           
 lsm303d_magnetometer   | varchar   |       | ["null","string"]                                                           
 __partition__          | integer   |       | The partition number which the message belongs to                           
 __event_time__         | timestamp |       | Application defined timestamp in milliseconds of when the event occurred    
 __publish_time__       | timestamp |       | The timestamp in milliseconds of when event as published                    
 __message_id__         | varchar   |       | The message ID of the message used to generate this row                     
 __sequence_id__        | bigint    |       | The sequence ID of the message used to generate this row                    
 __producer_name__      | varchar   |       | The name of the producer that publish the message used to generate this row 
 __key__                | varchar   |       | The partition key for the topic                                             
 __properties__         | varchar   |       | User defined properties                                                     
(37 rows)

presto> select * from pulsar."public/default"."pi-sensors";
        uuid        |   ipaddress   | cputempf | runtime | host  | hostname |    macaddress     |      endtime       |         te         | cpu | disk
--------------------+---------------+----------+---------+-------+----------+-------------------+--------------------+--------------------+-----+-----
 snr_20220323180318 | 192.168.1.229 |       99 |       4 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058598.8543017 | 4.47935152053833   | 0.2 | 3895
 snr_20220323180324 | 192.168.1.229 |       99 |      10 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058604.4054732 | 10.03052306175232  | 0.0 | 3895
 snr_20220323180329 | 192.168.1.229 |       99 |      16 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058609.8929565 | 15.518006324768066 | 6.5 | 3895
 snr_20220323180335 | 192.168.1.229 |       99 |      21 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058615.3783045 | 21.00335431098938  | 0.2 | 3895
 snr_20220323180340 | 192.168.1.229 |       99 |      26 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058620.8675282 | 26.49257802963257  | 4.6 | 3895
 snr_20220323180346 | 192.168.1.229 |       99 |      32 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058626.3639522 | 31.989001989364624 | 0.0 | 3895
 snr_20220323180351 | 192.168.1.229 |       99 |      38 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058631.8793604 | 37.50441026687622  | 0.0 | 3895
 snr_20220323180357 | 192.168.1.229 |      100 |      43 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058637.38347   | 43.008519887924194 | 0.0 | 3895
 snr_20220323180402 | 192.168.1.229 |       99 |      49 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058642.8820572 | 48.50710701942444  | 0.0 | 3895
 snr_20220323180408 | 192.168.1.229 |       99 |      54 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058648.3795574 | 54.00460720062256  | 6.2 | 3895
 snr_20220323180413 | 192.168.1.229 |       99 |      59 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058653.8280468 | 59.45309662818909  | 0.0 | 3895
 snr_20220323180419 | 192.168.1.229 |       99 |      65 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058659.3180714 | 64.94312119483948  | 4.9 | 3895
 snr_20220323180424 | 192.168.1.229 |       99 |      70 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058664.8023574 | 70.42740726470947  | 0.0 | 3895
 snr_20220323180430 | 192.168.1.229 |       99 |      76 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058670.286937  | 75.91198682785034  | 0.0 | 3895
 snr_20220323180435 | 192.168.1.229 |       97 |      81 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058675.7804654 | 81.40551519393921  | 0.0 | 3895
 snr_20220323180441 | 192.168.1.229 |       99 |      87 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058681.2751634 | 86.90021324157715  | 0.0 | 3895
 snr_20220323180446 | 192.168.1.229 |       99 |      92 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058686.7713509 | 92.39640069007874  | 5.9 | 3895
 snr_20220323180452 | 192.168.1.229 |       99 |      98 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058692.2672575 | 97.89230728149414  | 0.3 | 3895
 snr_20220323180457 | 192.168.1.229 |       99 |     103 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058697.7704427 | 103.39549255371094 | 5.4 | 3895
 snr_20220323180503 | 192.168.1.229 |       99 |     109 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058703.21333   | 108.83837985992432 | 0.3 | 3895
 snr_20220323180508 | 192.168.1.229 |       99 |     114 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058708.6879904 | 114.31304025650024 | 0.0 | 3895
 snr_20220323180514 | 192.168.1.229 |       99 |     120 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058714.1396198 | 119.76466965675354 | 0.3 | 3895
 snr_20220323180519 | 192.168.1.229 |       99 |     125 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058719.6158638 | 125.24091362953186 | 0.0 | 3895
 snr_20220323180525 | 192.168.1.229 |      100 |     131 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058725.0950723 | 130.72012209892273 | 6.5 | 3895
 snr_20220323180530 | 192.168.1.229 |       99 |     136 | piups | piups    | b8:27:eb:4a:4b:61 | 1648058730.57256   | 136.19760990142822 | 0.0 | 3895
(25 rows)

Query 20220323_184946_00003_p66fs, FINISHED, 1 node

````

![PULSARSQL](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorsprestotable.jpg)

![PULSARSQL](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorstable.jpg)

![PULSARSQL](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorstabletrino.jpg)

![PULSARSQL](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorstrinoresults.jpg)

![PULSARSQL](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pisensorstrinotabledef.jpg)




#### Spark SQL

````
val dfPulsar = spark.readStream.format("pulsar").option("service.url", "pulsar://pulsar1:6650").option("admin.url", "http://pulsar1:8080").option("topic", "persistent://public/default/pi-sensors").load()

scala> dfPulsar.printSchema()
root
 |-- uuid: string (nullable = true)
 |-- ipaddress: string (nullable = true)
 |-- cputempf: integer (nullable = true)
 |-- runtime: integer (nullable = true)
 |-- host: string (nullable = true)
 |-- hostname: string (nullable = true)
 |-- macaddress: string (nullable = true)
 |-- endtime: string (nullable = true)
 |-- te: string (nullable = true)
 |-- cpu: float (nullable = true)
 |-- diskusage: string (nullable = true)
 |-- memory: float (nullable = true)
 |-- rowid: string (nullable = true)
 |-- systemtime: string (nullable = true)
 |-- ts: integer (nullable = true)
 |-- starttime: string (nullable = true)
 |-- BH1745_red: float (nullable = true)
 |-- BH1745_green: float (nullable = true)
 |-- BH1745_blue: float (nullable = true)
 |-- BH1745_clear: float (nullable = true)
 |-- VL53L1X_distance_in_mm: float (nullable = true)
 |-- ltr559_lux: float (nullable = true)
 |-- ltr559_prox: float (nullable = true)
 |-- bme680_tempc: float (nullable = true)
 |-- bme680_tempf: float (nullable = true)
 |-- bme680_pressure: float (nullable = true)
 |-- bme680_humidity: float (nullable = true)
 |-- lsm303d_accelerometer: string (nullable = true)
 |-- lsm303d_magnetometer: string (nullable = true)
 |-- __key: binary (nullable = true)
 |-- __topic: string (nullable = true)
 |-- __messageId: binary (nullable = true)
 |-- __publishTime: timestamp (nullable = true)
 |-- __eventTime: timestamp (nullable = true)
 |-- __messageProperties: map (nullable = true)
 |    |-- key: string
 |    |-- value: string (valueContainsNull = true)


## Example Queries

val pQuery = dfPulsar.selectExpr("*").writeStream.format("console").option("truncate", false).start()

val pQuery = dfPulsar.selectExpr("CAST(__key AS STRING)", 
                                 "CAST(uuid AS STRING)",
                                 "CAST(ipaddress AS STRING)",
                                 "CAST(cputempf AS STRING)",
                                 "CAST(host AS STRING)",
                                 "CAST(cpu AS STRING)",
                                 "CAST(diskusage AS STRING)",
                                 "CAST(memory AS STRING)",
                                 "CAST(systemtime AS STRING)",
                                 "CAST(BH1745_red AS STRING)",
                                 "CAST(BH1745_green AS STRING)",
                                 "CAST(BH1745_blue AS STRING)",
                                 "CAST(BH1745_clear AS STRING)",
                                 "CAST(VL53L1X_distance_in_mm AS STRING)",
                                 "CAST(ltr559_lux AS STRING)",                                 
                                 "CAST(bme680_tempf AS STRING)",
                                 "CAST(bme680_pressure AS STRING)",
                                 "CAST(bme680_humidity AS STRING)")
                                 .as[(String, String, String, String, String, String, String, String,
                                 String, String, String, String, String, String, String, String, String, String)]
            .writeStream.format("csv")
            .option("truncate", "false")
            .option("header", true)
            .option("path", "/opt/demo/pisensordata")
            .option("checkpointLocation", "/tmp/checkpoint")
            .start()

## You could do csv, parquet, json, orc

pQuery.explain()
pQuery.awaitTermination()
pQuery.stop()

// can be "orc", "json", "csv", etc.

````

![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkexecutors.jpg)
![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkjobs.jpg)
![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkquerydetails.jpg)
![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparksqltest.jpg)
![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkstage.jpg)
![SPARK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkstreamingquerystats.jpg)


#### Example Spark ETL CSV Output

````
/opt/demo/pisensordata# cat part-00000-0425bfc8-5d25-4143-818c-bc7af5e1d82c-c000.csv
__key,uuid,ipaddress,cputempf,host,cpu,diskusage,memory,systemtime,BH1745_red,BH1745_green,BH1745_blue,BH1745_clear,VL53L1X_distance_in_mm,ltr559_lux,bme680_tempf,bme680_pressure,bme680_humidity
snr_20220324215723,snr_20220324215723,192.168.1.229,95,piups,0.0,3887.5 MB,20.6,03/24/2022 17:57:24,134.2,99.0,75.6,130.0,15.0,6.09,70.66,1006.11,44.737

````

![CSV](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/sparkcsvoutput.jpg)


#### Flink SQL

````
CREATE CATALOG pulsar WITH (
   'type' = 'pulsar',
   'service-url' = 'pulsar://pulsar1:6650',
   'admin-url' = 'http://pulsar1:8080',
   'format' = 'json'
);

USE CATALOG pulsar;

SHOW TABLES;


describe `pi-sensors`;
> 
+------------------------+--------+------+-----+--------+-----------+
|                   name |   type | null | key | extras | watermark |
+------------------------+--------+------+-----+--------+-----------+
|                   uuid | STRING | true |     |        |           |
|              ipaddress | STRING | true |     |        |           |
|               cputempf |    INT | true |     |        |           |
|                runtime |    INT | true |     |        |           |
|                   host | STRING | true |     |        |           |
|               hostname | STRING | true |     |        |           |
|             macaddress | STRING | true |     |        |           |
|                endtime | STRING | true |     |        |           |
|                     te | STRING | true |     |        |           |
|                    cpu |  FLOAT | true |     |        |           |
|              diskusage | STRING | true |     |        |           |
|                 memory |  FLOAT | true |     |        |           |
|                  rowid | STRING | true |     |        |           |
|             systemtime | STRING | true |     |        |           |
|                     ts |    INT | true |     |        |           |
|              starttime | STRING | true |     |        |           |
|             BH1745_red |  FLOAT | true |     |        |           |
|           BH1745_green |  FLOAT | true |     |        |           |
|            BH1745_blue |  FLOAT | true |     |        |           |
|           BH1745_clear |  FLOAT | true |     |        |           |
| VL53L1X_distance_in_mm |  FLOAT | true |     |        |           |
|             ltr559_lux |  FLOAT | true |     |        |           |
|            ltr559_prox |  FLOAT | true |     |        |           |
|           bme680_tempc |  FLOAT | true |     |        |           |
|           bme680_tempf |  FLOAT | true |     |        |           |
|        bme680_pressure |  FLOAT | true |     |        |           |
|        bme680_humidity |  FLOAT | true |     |        |           |
|  lsm303d_accelerometer | STRING | true |     |        |           |
|   lsm303d_magnetometer | STRING | true |     |        |           |
+------------------------+--------+------+-----+--------+-----------+

select max(bme680_pressure) as maxpressure, max(bme680_tempf) as maxtemp, max(ltr559_lux) as maxlux, avg(BH1745_red) as avgred,
       max(VL53L1X_distance_in_mm) as maxdistance
from `pi-sensors`

select * from `pi-sensors`;

````


![FLINK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/flinkrowsummary.jpg)
![FLINK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/flinksqlclienttop.jpg)
![FLINK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/flinksqlcontinuous.jpg)
![FLINK](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/flinksqlmax.jpg)


### Apache NiFi - Pulsar Consumer.   MongoDB Writer.

![NIFI](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/nifigroup.jpg)

![NIFI](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/nififlow.jpg)

![NIFI](https://raw.githubusercontent.com/tspannhw/FLiP-Pi-BreakoutGarden/main/images/consumePulsarRecod.jpg)

![NIFI](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/nifiqueryrecord.jpg)

![NIFI](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/putMongoRecord.jpg)

![NIFI](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/nifimongocontroller.jpg)


### Data Store - MongoDB

````

mongo -u debezium -p dbz --authenticationDatabase admin pulsar1:27017/inventory

show databases

db.createCollection("pisensors")

show collections

db.pisensors.find().pretty()

db.pisensors.find().pretty()
{
        "_id" : ObjectId("623b812e5dae8913d42a93ee"),
        "uuid" : "snr_20220323194514",
        "ipaddress" : "192.168.1.229",
        "cputempf" : 100,
        "runtime" : 9,
        "host" : "piups",
        "hostname" : "piups",
        "macaddress" : "b8:27:eb:4a:4b:61",
        "endtime" : "1648064714.7820184",
        "te" : "9.371636629104614",
        "cpu" : 6.5,
        "diskusage" : "3895.4 MB",
        "memory" : 21.4,
        "rowid" : "20220323194514_c9ec900f-05c2-49c4-985f-ddd83e8b15c0",
        "systemtime" : "03/23/2022 15:45:15",
        "ts" : 1648064715,
        "starttime" : "03/23/2022 15:45:05",
        "BH1745_red" : 112.2,
        "BH1745_green" : 83,
        "BH1745_blue" : 64.8,
        "BH1745_clear" : 110,
        "VL53L1X_distance_in_mm" : 31,
        "ltr559_lux" : 6.65,
        "ltr559_prox" : 0,
        "bme680_tempc" : 23.47,
        "bme680_tempf" : 74.25,
        "bme680_pressure" : 1017.71,
        "bme680_humidity" : 34.432,
        "lsm303d_accelerometer" : "-00.08g : -01.01g : +00.01g",
        "lsm303d_magnetometer" : "+00.06 : +00.30 : +00.07"
}

````

![MongoData](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/mongoprettydata.jpg)


### Monitor Everything!   Let me see what's going on!?!??!

![GRAFANA](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/grafana.jpg)

![GRAFANA](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/grafana2.jpg)

![GRAFANA](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/grafana3.jpg)

[!PULSARMAN](https://github.com/tspannhw/FLiP-Pi-BreakoutGarden/blob/main/images/pulsarman.jpg)


### References

* https://www.academy.streamnative.io/
* https://github.com/tspannhw/PulsarOnRaspberryPi
* https://community.cloudera.com/t5/Community-Articles/IoT-Series-Sensors-Utilizing-Breakout-Garden-Hat-Part-1/ta-p/249262
* https://shop.pimoroni.com/products/breakout-garden-hat?variant=12767628787795
* https://github.com/pimoroni/breakout-garden
* https://github.com/pimoroni/bme680-python
* https://github.com/pimoroni/bh1745-python
* https://github.com/pimoroni/vl53l1x-python
* https://github.com/pimoroni/ltr559-python
* https://github.com/pimoroni/lsm303d-python
* https://github.com/rm-hull/luma.oled
* https://luma-oled.readthedocs.io/en/latest/install.html
* https://github.com/streamnative/examples/blob/master/cloud/python/OAuth2Consumer.py
* https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#output-sinks
