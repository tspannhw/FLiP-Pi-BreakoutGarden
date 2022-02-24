import argparse
import pulsar
import logging
from pulsar.schema import *
from pulsar.schema import AvroSchema
from pulsar.schema import JsonSchema
from pulsar import Client, AuthenticationOauth2
import breakoutsensorschema
from breakoutsensorschema import breakoutsensor

parse = argparse.ArgumentParser(prog='consumer.py')
parse.add_argument('-su', '--service-url', dest='service_url', type=str, required=True,
                   help='The pulsar service you want to connect to')
parse.add_argument('-t', '--topic', dest='topic', type=str, required=True,
                   help='The topic you want to produce to')
parse.add_argument('-n', '--number', dest='number', type=int, default=1,
                   help='The number of message you want to produce')
parse.add_argument('--auth-params', dest='auth_params', type=str, default="",
                   help='The auth params which you need to configure the client')
args = parse.parse_args()

print(args.service_url)
print(args.auth_params)

client = pulsar.Client(args.service_url, authentication=AuthenticationOauth2(args.auth_params))
# producer = client.create_producer(topic=args.topic ,schema=JsonSchema(breakoutsensor),properties={"producer-name": "sensor-py-sensor","producer-id": "sensor-sensor" })

counter = 5000

sub = client.subscribe(args.topic, "testtimsub", schema=JsonSchema(breakoutsensor))

while counter > 0:
    try:
        msg = sub.receive()
#        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
        newRecord = msg.value()
        print(newRecord)
        # Acknowledge successful processing of the message
        sub.acknowledge(msg)
        counter -= 1
    except:
        # Message failed to be processed
        sub.negative_acknowledge(msg)
