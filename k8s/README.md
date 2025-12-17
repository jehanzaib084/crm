# Kubernetes Deployment Configuration

This directory contains Kubernetes manifests for deploying the CRM application.

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured to access your cluster
- Docker registry access
- Sufficient cluster resources

## Quick Start

### 1. Create Namespace

```bash
kubectl create namespace crm-production
```

### 2. Create Secrets

Copy the example secrets file and update with your values:

```bash
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your actual values
kubectl apply -f secrets.yaml -n crm-production
```

**IMPORTANT**: Never commit `secrets.yaml` to version control!

### 3. Create Docker Registry Secret (for private registries)

```bash
kubectl create secret docker-registry docker-registry-secret \
  --docker-server=docker.io \
  --docker-username=your-username \
  --docker-password=your-password \
  --docker-email=your-email@example.com \
  -n crm-production
```

### 4. Build and Push Docker Images (First Time)

**IMPORTANT**: Before deploying, you must build and push Docker images first, or update the image names in the deployment YAML files to valid images.

Option A - Using Jenkins pipeline (recommended):
```bash
# Run the Jenkins pipeline once to build and push images
# The pipeline will automatically update the deployments
```

Option B - Manual build and push:
```bash
# Build images
cd ..
docker build -t your-registry/your-namespace/crm-backend:latest ./backend
docker build -t your-registry/your-namespace/crm-frontend:latest ./frontend
docker build -t your-registry/your-namespace/crm-database:latest ./db

# Push to registry
docker push your-registry/your-namespace/crm-backend:latest
docker push your-registry/your-namespace/crm-frontend:latest
docker push your-registry/your-namespace/crm-database:latest

# Update image names in deployment files
# Edit backend-deployment.yaml, frontend-deployment.yaml with your actual image names
cd k8s
```

### 5. Deploy Application

Apply configurations in order:

```bash
# Apply ConfigMaps
kubectl apply -f configmap.yaml -n crm-production

# Deploy MongoDB
kubectl apply -f mongodb-deployment.yaml -n crm-production

# Wait for MongoDB to be ready
kubectl wait --for=condition=ready pod -l app=mongodb -n crm-production --timeout=300s

# Deploy Backend (ensure image name is correct in the YAML)
kubectl apply -f backend-deployment.yaml -n crm-production

# Deploy Frontend (ensure image name is correct in the YAML)
kubectl apply -f frontend-deployment.yaml -n crm-production

# Optional: Deploy Ingress (requires Ingress controller)
kubectl apply -f ingress.yaml -n crm-production
```

## Configuration Files

### Core Deployments

- **mongodb-deployment.yaml**: MongoDB database deployment with persistent storage
- **backend-deployment.yaml**: Node.js/Express backend API deployment
- **frontend-deployment.yaml**: React frontend deployment with nginx

### Configuration

- **configmap.yaml**: Application configuration (non-sensitive)
- **secrets.yaml.example**: Template for sensitive configuration (JWT secrets, DB passwords, etc.)
- **ingress.yaml**: Optional ingress configuration for production

## Accessing the Application

### Using LoadBalancer (default)

```bash
# Get frontend service external IP
kubectl get svc crm-frontend -n crm-production

# Access the application at http://<EXTERNAL-IP>
```

### Using Ingress

1. Ensure you have an Ingress controller installed (e.g., nginx-ingress)
2. Update `ingress.yaml` with your domain name
3. Apply the ingress configuration
4. Configure DNS to point to your ingress controller

### Using Port Forward (for testing)

```bash
# Frontend
kubectl port-forward svc/crm-frontend 3000:80 -n crm-production

# Backend
kubectl port-forward svc/crm-backend 8888:8888 -n crm-production

# Access at http://localhost:3000
```

## Monitoring Deployment

### Check Pod Status

```bash
kubectl get pods -n crm-production
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/crm-backend -n crm-production

# Frontend logs
kubectl logs -f deployment/crm-frontend -n crm-production

# MongoDB logs
kubectl logs -f deployment/mongodb -n crm-production
```

### Describe Resources

```bash
kubectl describe deployment crm-backend -n crm-production
kubectl describe pod <pod-name> -n crm-production
```

## Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment crm-backend --replicas=3 -n crm-production

# Scale frontend
kubectl scale deployment crm-frontend --replicas=3 -n crm-production
```

### Horizontal Pod Autoscaler (HPA)

```bash
# Auto-scale based on CPU
kubectl autoscale deployment crm-backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n crm-production
```

## Updating Images

### Manual Update

```bash
kubectl set image deployment/crm-backend \
  crm-backend=your-registry/your-namespace/crm-backend:new-tag \
  -n crm-production

kubectl rollout status deployment/crm-backend -n crm-production
```

### Rollback

```bash
# View rollout history
kubectl rollout history deployment/crm-backend -n crm-production

# Rollback to previous version
kubectl rollout undo deployment/crm-backend -n crm-production

# Rollback to specific revision
kubectl rollout undo deployment/crm-backend --to-revision=2 -n crm-production
```

## Troubleshooting

### Pods Not Starting

```bash
# Check events
kubectl get events -n crm-production --sort-by='.lastTimestamp'

# Describe pod
kubectl describe pod <pod-name> -n crm-production

# Check logs
kubectl logs <pod-name> -n crm-production --previous
```

### Connection Issues

```bash
# Test backend connectivity from frontend pod
kubectl exec -it <frontend-pod-name> -n crm-production -- wget -O- http://crm-backend:8888/api/ping

# Test MongoDB connectivity from backend pod
kubectl exec -it <backend-pod-name> -n crm-production -- node -e "const mongoose = require('mongoose'); mongoose.connect(process.env.DATABASE).then(() => console.log('Connected')).catch(err => console.error(err));"
```

### Resource Issues

```bash
# Check resource usage
kubectl top pods -n crm-production
kubectl top nodes
```

## Cleanup

### Delete All Resources

```bash
kubectl delete namespace crm-production
```

### Delete Specific Resources

```bash
kubectl delete -f . -n crm-production
```

## Production Considerations

1. **Persistent Volumes**: Ensure proper backup strategy for MongoDB PVC
2. **Resource Limits**: Adjust based on your workload
3. **High Availability**: Run multiple replicas and use pod anti-affinity
4. **Monitoring**: Integrate with Prometheus/Grafana
5. **Secrets Management**: Consider using external secret management (Vault, AWS Secrets Manager)
6. **SSL/TLS**: Use cert-manager for automatic certificate management
7. **Database**: Consider managed database service for production
8. **Backups**: Implement regular database backups
9. **Network Policies**: Restrict pod-to-pod communication
10. **Security Context**: Run containers as non-root user

## CI/CD Integration

These manifests are designed to work with the Jenkins pipeline defined in the root `Jenkinsfile`. The pipeline automatically:

1. Builds Docker images
2. Pushes to registry
3. Updates Kubernetes deployments
4. Verifies deployment health

See the root `Jenkinsfile` for pipeline configuration.
