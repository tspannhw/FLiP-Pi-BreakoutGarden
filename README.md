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

### Software / Libraries

* Python 3.9 
* Pulsar Python Client 2.10 (avro) pip3 install pulsar-client[avro]
* Python Breakout Garden
* Python PSUTIL https://pypi.org/project/psutil/
* Python LUMA OLED pip3 install --upgrade luma.oled
* Libraries sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y

### StreamOps

````
bin/pulsar-admin topics create "persistent://public/default/pi-sensors"

````

### Consumer

````

bin/pulsar-client consume "persistent://public/default/pi-sensors" -s "pisnsrgrdnrdr" -n 0


````

### SQL Consumers

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
#### Spark SQL

````
val dfPulsar = spark.readStream.format("pulsar").option("service.url", "pulsar://pulsar1:6650").option("admin.url", "http://pulsar1:8080").option("topic", "persistent://public/default/pi-sensors").load()
dfPulsar.printSchema()
val pQuery = dfPulsar.selectExpr("*").writeStream.format("csv").option("truncate", false) .option("checkpointLocation", "/tmp/checkpoint").option("path", "/opt/demo/pisensors").start()
    
pQuery.explain()
pQuery.awaitTermination()
pQuery.stop()

// can be "orc", "json", "csv", etc.


````

#### Flink SQL

````
REATE CATALOG pulsar WITH (
   'type' = 'pulsar',
   'service-url' = 'pulsar://pulsar1:6650',
   'admin-url' = 'http://pulsar1:8080',
   'format' = 'json'
);

USE CATALOG pulsar;

SHOW TABLES;

Flink SQL> describe garden3;

````

### Data Store - MongoDB

````
mongodb://pulsar1:27017


mongo -u debezium -p dbz --authenticationDatabase admin pulsar1:27017/inventory

show databases

db.createCollection("pisensors")

show collections

db.pisensors.find().pretty()

````

### References

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


