#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

CLUSTER_NAME="ai-platform"

echo "========================================"
echo "AI Platform Development Environment"
echo "========================================"

echo
echo "[1/6] Checking Docker..."

docker info >/dev/null

echo "Docker is available."

echo
echo "[2/6] Checking Kubernetes cluster..."

if ! kind get clusters | grep -qx "$CLUSTER_NAME"; then

    echo "Creating Kind cluster..."

    kind create cluster \
        --name "$CLUSTER_NAME" \
        --config infra/kind/cluster.yaml

else

    echo "Kind cluster already exists."

fi

echo
echo "[3/6] Waiting for cluster..."

kubectl cluster-info

echo
echo "[4/6] Applying OpenTelemetry Collector..."

kubectl apply \
    -f deployments/observability/otel-collector/configmap.yaml

kubectl apply \
    -f deployments/observability/otel-collector/deployment.yaml

kubectl apply \
    -f deployments/observability/otel-collector/service.yaml

echo
echo "[5/6] Applying AI Platform API..."

kubectl apply \
    -f deployments/api/deployment.yaml

kubectl apply \
    -f deployments/api/service.yaml

echo
echo "[6/6] Waiting for workloads..."

kubectl rollout status deployment/otel-collector

kubectl rollout status deployment/ai-platform-api

echo
echo "========================================"
echo "Environment is ready"
echo "========================================"

echo

kubectl get pods

echo

kubectl get services