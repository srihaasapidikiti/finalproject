from flask import Flask, request, Response
import jsonpickle
import pika
import io
import redis
import base64
import sys

# Initialize the Flask application
app = Flask(__name__)
connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
redisByReviews = redis.Redis(host='redis', port=6379, db=1)
f = open(sys.argv[1], 'r')
line = f.readline()
hname = line.split()[0]
#hname = str(sys.argv[1])
# route http posts to this method

@app.route('/api/review', methods=['POST'])
def test():
    r = request
    print(r.data)
    args = request.args
    # convert the data to a PIL image type so we can extract dimensions
    try:  
        x = str(args['X'])
        words2=x.split("-")
        sending1 = {
            'restaurant': words2[0],
            'locality': words2[1],
            'cuisine': words2[2],
            'cost': words2[3],
            'rating': words2[4] 
        }   
        print('sending1to')
        sending_pickled = jsonpickle.encode(sending1) 
        #channel.exchange_declare(exchange='toWorker', exchange_type='direct')
        channel.queue_declare(queue='toWorker', durable=True)
        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
        key1 = hname+'.rest.logs'
        #severity = hash1
        #message = hash1
        channel.basic_publish(
            exchange='', routing_key='toWorker', body=sending_pickled)
        channel.basic_publish(
            exchange='topic_logs', routing_key=key1, body='review sent succesfully to worker')    
        #print(" [x] Sent %r:%r" % (key1, hash1))
    # build a response dict to send back to client
        response = {
            'status': "added"
            }
        
    except:
        response = {'status': 0}
        channel.basic_publish(
            exchange='topic_logs', routing_key=hname+'.rest.debug', body='failed sending image to worker')
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")
    
	
@app.route('/getrestaurant/<locality>/<cuisines>/<cost>', methods=['GET'])
def test1(locality, cuisines, cost):
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    #ioBuffer = io.BytesIO(r.data)
    args = request.args
    try:
        #x= str(args['X'])
        List=[]
        List1=[]
        l1=locality
        c1=cuisines
        c2=cost
        words= (c2.split("-"))
        x1= int(words[0])
        x2= int(words[1])
        i=x1
        while(i<=x2):
            List.append(str(i))
            print(i)
            i=i+100          
        
        print(l1)
        str1=""
        for i in range(0,len(List)):
            print(List[i]) 
            s = redisByReviews.sinter(l1,c1,List[i])
            print(s)
            #l = sorted(s)
            for i in s:
                x = redisByReviews.hgetall(i.decode("utf-8"))
                r2= x[b'Restaurant'].decode('utf-8')
                print(r2)
                r3= x[b'Rating'].decode('utf-8')
                List1.append(r2+"/"+r3+" ")
                print(List1)
    # build a response dict to send back to client
        response = {
                    'Restaurant/Rating': List1                   
                }
       # channel.basic_publish(
       #     exchange='topic_logs', routing_key=hname+'.rest.logs', body='checked successfully for hash in database')        
    except:
        response = {'Restaurant':None}
        #channel.basic_publish(
        #    exchange='topic_logs', routing_key=hname+'.rest.debug', body='failed checking hash value')
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
 


# start flask app
app.run(host="0.0.0.0", port=5000)