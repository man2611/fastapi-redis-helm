#!/bin/bash

#!/bin/bash

kubectl apply -f k8s/redis-configmap.yaml
kubectl apply -f k8s/redis-secret.yaml
kubectl apply -f k8s/redis-pvc.yaml
kubectl apply -f k8s/redis-deployments.yaml
kubectl apply -f k8s/redis-service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml