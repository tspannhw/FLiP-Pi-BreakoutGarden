# cloud run   https://github.com/streamnative/examples/tree/master/cloud/python


python3 /opt/demo/breakoutsensor.py -su pulsar+ssl://sn-academy.x.snio.cloud:6651 -t persistent://public/default/pi-sensors --auth-params '{"issuer_url":"https://auth.x.cloud", "private_key":"x-tspann.json", "audience":"urn:sn:pulsar:x:my-instance"}' 
