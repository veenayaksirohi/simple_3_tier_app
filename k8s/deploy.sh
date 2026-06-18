#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "Deleting old resources..."

kubectl delete -f frontend-deployment.yaml --ignore-not-found
kubectl delete -f frontend-service.yaml --ignore-not-found
kubectl delete -f backend-deployment.yaml --ignore-not-found
kubectl delete -f backend-service.yaml --ignore-not-found
kubectl delete -f database-deployment.yaml --ignore-not-found
kubectl delete -f database-service.yaml --ignore-not-found

echo "Deploying resources..."

kubectl apply -f namespace.yaml

kubectl apply -f database-deployment.yaml
kubectl apply -f database-service.yaml

kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml

kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

echo "Deployment completed."

kubectl get all -n web-app
