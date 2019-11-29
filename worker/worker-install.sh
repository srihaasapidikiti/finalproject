#!/bin/sh
#
# This is the script you need to provide to install the rest-server.py and start it running.
# It will be provided to the instance using redis-launch.sh
#
#!/bin/sh
#
# The following script should install OpenALPR using apt-get
# in Ubuntu 19.10. There's an error in the configuration that needs
# to be addressed manually
#
# Install prerequisites
apt-get update
export DEBIAN_FRONTEND=noninteractive 

# Install other packages as needed
#
#apt-get install 
apt-get install -y python3 python3-pip  python3-pillow python3-openalpr python3-redis
pip3 install pika
pip3 install jsonpickle
pip3 install pillow
pip3 install requests
pip3 install redis

curl http://metadata/computeMetadata/v1/instance/attributes/worker-client -H "Metadata-Flavor: Google" > worker-client.py
hostname=$(curl http://metadata.google.internal/computeMetadata/v1/instance/hostname -H "Metadata-Flavor:Google" | cut -d . -f1) 

echo 'starting'
nohup python3 -u worker-client.py $hostname &
#sudo python3 worker-client.py image1