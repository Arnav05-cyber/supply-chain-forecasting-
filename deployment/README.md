# Deployment Configurations

Docker and Kubernetes deployment files.

## Files
- `docker_scaling_setup.py` - Docker setup script
- `kubernetes_deployment.yaml` - K8s configuration

## Usage
```bash
# Docker
python docker_scaling_setup.py
docker-compose up

# Kubernetes  
kubectl apply -f kubernetes_deployment.yaml
```
