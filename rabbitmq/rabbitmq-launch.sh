#!/bin/sh
#
# This is the script you need to provide to launch a rabbitmq instance
# and cause it to run the rabbitmq-install.sh script
#
#gclud config set project "green-entity-251200"
gcloud compute --project=green-entity-251200 instances create rabbitmq --tags=default-allow-internal --zone=us-west1-a --machine-type=n1-standard-1 --network-interface=no-address --image=ubuntu-1804-bionic-v20191021 --image-project=ubuntu-os-cloud --metadata-from-file=startup-script=rabbitmq-install.sh
