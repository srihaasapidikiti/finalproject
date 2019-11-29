#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and cause it to run the redis-install.sh script
#
gcloud compute instances create rest --zone=us-west1-a --machine-type=n1-standard-1  --image=ubuntu-1804-bionic-v20191021 --image-project=ubuntu-os-cloud --metadata-from-file=startup-script=rest-install.sh,rest-server=rest-server.py

#gcloud compute scp --zone us-west1-a rest-server.py rest:~/
#gcloud compute ssh --zone us-west1-a rest --command 'sudo sh rest-install.sh'