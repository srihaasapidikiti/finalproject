#!/bin/sh
#
# This is the script you need to provide to install the rest-server.py and start it running.
# It will be provided to the instance using redis-launch.sh
#
sudo apt-get install openssh-server
sudo ufw allow 22
apt-get update
apt-get install -y python3 python3-pip git

#cd ~/.
#git clone https://github.com/pallets/flask
#cd ~/flask/examples/tutorial
#sudo python3 setup.py install


#export FLASK_APP=flaskr
#flask init-db
#nohup flask run -h 0.0.0.0 &
#cd ~/.
#gsutil cp gs://bucket1h/rest-server.py rest-server.py
echo done
#git clone https://github.com/srihaasapidikiti/part7ex.git
#cd part7ex
sudo pip3 install -U Flask
#sudo pip3 install -e .
sudo pip3 install requests
sudo pip3 install jsonpickle
pip3 install pika
echo jsonpickle
sudo pip3 install pillow
pip3 install redis
#r1= $(curl http://metadata/computeMetadata/v1/instance/attributes/rest-server -H "Metadata-Flavor: Google")
curl http://metadata/computeMetadata/v1/instance/attributes/rest-server -H "Metadata-Flavor: Google" > rest-server.py
curl http://metadata.google.internal/computeMetadata/v1/instance/hostname -H "Metadata-Flavor:Google" | cut -d . -f1 > hostname.txt
#cat > rest-server1.py << EOF
#$r1
#EOF
#echo done
#echo $hostname
sudo python3 -u rest-server.py hostname.txt