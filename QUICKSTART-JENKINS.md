# Jenkins Pipeline Quick Start Guide

This is a quick reference guide to get your Jenkins pipeline up and running fast. For detailed documentation, see [JENKINS.md](./JENKINS.md).

## 🚀 Quick Setup (5 Minutes)

### Step 1: Update Jenkinsfile Configuration

Edit the `Jenkinsfile` and update these lines:

```groovy
// Line 6-7: Set your Docker registry
DOCKER_REGISTRY = 'docker.io'  // Your registry URL
DOCKER_NAMESPACE = 'your-dockerhub-username'  // Your Docker Hub username

// Line 21: Set your Kubernetes namespace
K8S_NAMESPACE = 'crm-production'  // Your desired namespace
```

### Step 2: Create Jenkins Credentials

#### Docker Registry Credentials
1. Go to Jenkins → Manage Jenkins → Credentials → Global → Add Credentials
2. **Kind**: Username with password
3. **ID**: `docker-registry-credentials`
4. **Username**: Your Docker Hub username
5. **Password**: Your Docker Hub password/token

#### Kubernetes Config
1. Go to Jenkins → Manage Jenkins → Credentials → Global → Add Credentials
2. **Kind**: Secret file
3. **ID**: `kubeconfig-credentials`
4. **File**: Upload your `~/.kube/config` file

### Step 3: Setup Kubernetes

```bash
# Create namespace
kubectl create namespace crm-production

# Create secrets
cd k8s
cp secrets.yaml.example secrets.yaml
# Edit secrets.yaml with your values
kubectl apply -f secrets.yaml -n crm-production

# Create Docker registry secret
kubectl create secret docker-registry docker-registry-secret \
  --docker-server=docker.io \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD \
  --docker-email=YOUR_EMAIL \
  -n crm-production

# Apply ConfigMaps
kubectl apply -f configmap.yaml -n crm-production
```

### Step 4: Create Jenkins Job

1. Jenkins → New Item
2. Name: `crm-pipeline`
3. Type: **Pipeline**
4. Configuration:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your repository URL
   - **Branch**: `*/main`
   - **Script Path**: `Jenkinsfile`
5. Save

### Step 5: Run Pipeline

1. Click "Build Now"
2. Monitor progress in Console Output

## 📋 What the Pipeline Does

1. ✅ **Checkout**: Clone repository
2. ✅ **Install Dependencies**: Install npm packages for frontend & backend
3. ✅ **Lint**: Check code quality
4. ✅ **Build**: Build frontend production bundle
5. ✅ **Test**: Run automated tests
6. ✅ **Docker Build**: Create Docker images for all services
7. ✅ **Docker Push**: Push images to registry
8. ✅ **Deploy**: Deploy to Kubernetes
9. ✅ **Verify**: Check deployment health

## 🔍 Quick Verification

Check deployment status:

```bash
# View all pods
kubectl get pods -n crm-production

# View services
kubectl get svc -n crm-production

# View deployment status
kubectl rollout status deployment/crm-backend -n crm-production
kubectl rollout status deployment/crm-frontend -n crm-production

# View logs
kubectl logs -f deployment/crm-backend -n crm-production
kubectl logs -f deployment/crm-frontend -n crm-production
```

## 🌐 Access Your Application

### Option 1: LoadBalancer (default)
```bash
# Get external IP
kubectl get svc crm-frontend -n crm-production
# Access at http://<EXTERNAL-IP>
```

### Option 2: Port Forward (testing)
```bash
kubectl port-forward svc/crm-frontend 3000:80 -n crm-production
# Access at http://localhost:3000
```

### Option 3: Ingress (production)
```bash
kubectl apply -f k8s/ingress.yaml -n crm-production
# Configure DNS to point to ingress controller
```

## 🔧 Common Issues

### Issue: Docker push fails
**Solution**: Check Docker registry credentials in Jenkins

### Issue: Kubernetes deployment fails
**Solution**: Verify kubeconfig file is correct and you have cluster access

### Issue: Pods not starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n crm-production

# Check logs
kubectl logs <pod-name> -n crm-production
```

### Issue: Can't connect to backend
**Solution**: Verify MongoDB is running and backend can connect
```bash
kubectl logs deployment/mongodb -n crm-production
kubectl logs deployment/crm-backend -n crm-production
```

## 🎯 Next Steps

- [ ] Setup automatic builds with webhooks
- [ ] Configure email/Slack notifications
- [ ] Add staging environment
- [ ] Setup monitoring (Prometheus/Grafana)
- [ ] Configure backup for MongoDB

## 📚 Full Documentation

- [Complete Jenkins Guide](./JENKINS.md)
- [Kubernetes Deployment Guide](./k8s/README.md)
- [Project README](./README.md)

## 🆘 Need Help?

1. Check Jenkins console output for errors
2. Review pod logs: `kubectl logs <pod-name> -n crm-production`
3. Check this guide and full documentation
4. Contact DevOps team

---

**Tip**: For automatic builds on git push, setup a GitHub webhook pointing to `http://your-jenkins-url/github-webhook/`
