#!/usr/bin/env python
import pika
import sys
import jsonpickle
import json
import io
import pickle
import redis

connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()
channel.queue_declare(queue='toWorker', durable=True)
#channel.exchange_declare(exchange='toWorker', exchange_type='direct')
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
#result = channel.queue_declare('', exclusive=True)
#queue_name = result.method.queue
redisByReviews = redis.Redis(host='redis', port=6379, db=1)
hname= sys.argv[1]
#binding_keys = sys.argv[1:]
#if not binding_keys:
#    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
#    sys.exit(1)

#for binding_key in binding_keys:
#    channel.queue_bind(
#        exchange='toWorker', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    dict1= jsonpickle.decode(body)
    restaurant1 = str(dict1['restaurant'])
    locality1 = str(dict1['locality'])
    cuisine1 = str(dict1['cuisine'])
    cost1 = str(dict1['cost'])
    rating1 = str(dict1['rating'])
    i1=int(redisByReviews.dbsize())+1
    redisByReviews.hmset("reviews:"+str(i1), {"Restaurant": restaurant1,"Locality": locality1, "Cuisines": cuisine1,"Cost": cost1,"Rating": rating1 })
    redisByReviews.sadd(restaurant1, "reviews:"+str(i1))
    redisByReviews.sadd(locality1, "reviews:"+str(i1))
    redisByReviews.sadd(cuisine1, "reviews:"+str(i1))
    redisByReviews.sadd(cost1, "reviews:"+str(i1))
    redisByReviews.sadd(rating1, "reviews:"+str(i1))
    print("added")
    channel.basic_publish(
            exchange='topic_logs', routing_key=hname+'.worker.logs', body='successfully added to redisByReviews')
              
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='toWorker', on_message_callback=callback)
#channel.basic_consume(
#    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()