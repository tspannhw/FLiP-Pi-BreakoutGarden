# cloud run   https://github.com/streamnative/examples/tree/master/cloud/python

python3 /opt/demo/breakoutsensor.py -su pulsar+ssl://mycloud.snio.cloud:6651 -t persistent://public/default/pi-sensors --auth-params '{"issuer_url":"https://auth.streamnative.cloud", "private_key":"mysn-someguy.json", "audience":"urn:sn:pulsar:somecloud:my-instance"}' 

