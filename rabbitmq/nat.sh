gcloud compute --project="green-entity-251200" routers create nat-router --network=default --region=us-west1
gcloud compute --project="green-entity-251200" routers nats create nat-config \
    --router=nat-router \
    --region=us-west1\
    --auto-allocate-nat-external-ips \
    --nat-all-subnet-ip-ranges \