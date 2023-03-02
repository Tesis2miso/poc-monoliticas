




import pulsar

client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe('evento-orden',
                            subscription_name='evento-orden')

while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()