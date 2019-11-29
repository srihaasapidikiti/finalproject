#!/bin/sh
#
# This is the script you need to provide to launch a redis instance
# and cause it to run the redis-install.sh script
#

gcloud compute --project=green-entity-251200 instances create worker  --zone=us-west1-a --machine-type=n1-standard-1 --network-interface=no-address --image=ubuntu-minimal-1910-eoan-v20191022 --image-project=ubuntu-os-cloud --metadata-from-file=startup-script=worker-install.sh,worker-client=worker-client.py

#gcloud compute instances stop worker
