# Jenkins Pipeline Setup Guide

This document explains how to set up and use the Jenkins pipeline for the IDURAR CRM/ERP application.

## Overview

The Jenkins pipeline automates the following stages:
1. **Build Stage** - Builds both frontend and backend applications
2. **Automated Tests** - Runs health checks and linting
3. **Docker Build & Push** - Creates and pushes Docker images to registry
4. **Kubernetes Deployment** - Deploys the application to Kubernetes cluster

## Prerequisites

Before using this pipeline, ensure you have:

1. **Jenkins Server** with the following plugins:
   - Pipeline plugin
   - Docker plugin
   - Kubernetes plugin
   - Credentials plugin

2. **Docker Registry** (Docker Hub, AWS ECR, Azure ACR, or private registry)

3. **Kubernetes Cluster** (EKS, GKE, AKS, or on-premise)

4. **Required Tools** installed on Jenkins agent:
   - Node.js (v20.9.0)
   - npm (v10.2.4)
   - Docker
   - kubectl

## Jenkins Credentials Setup

Configure the following credentials in Jenkins (Manage Jenkins → Credentials):

### 1. Docker Registry Credentials

**Credential ID**: `docker-credentials-id`
- Type: Username with password
- Username: Your Docker registry username
- Password: Your Docker registry password or access token

### 2. Docker Registry URL

**Credential ID**: `docker-registry-url`
- Type: Secret text
- Secret: Your Docker registry URL (e.g., `docker.io` for Docker Hub, or your private registry URL)

### 3. Kubeconfig Credentials

**Credential ID**: `kubeconfig-credentials-id`
- Type: Secret file
- File: Your kubeconfig file for Kubernetes cluster access

## Configuration Steps

### Step 1: Update Docker Registry URLs

Edit the `Jenkinsfile` and update the following environment variables:

```groovy
environment {
    DOCKER_REGISTRY = credentials('docker-registry-url')
    DOCKER_CREDENTIALS = credentials('docker-credentials-id')
    BACKEND_IMAGE = "${DOCKER_REGISTRY}/idurar-backend"  // Update with your registry path
    FRONTEND_IMAGE = "${DOCKER_REGISTRY}/idurar-frontend"  // Update with your registry path
}
```

Example for Docker Hub:
```groovy
BACKEND_IMAGE = "yourusername/idurar-backend"
FRONTEND_IMAGE = "yourusername/idurar-frontend"
```

### Step 2: Update Kubernetes Manifests

The Kubernetes manifests use a placeholder `DOCKER_REGISTRY_PLACEHOLDER` which will be automatically replaced by the Jenkins pipeline with your actual registry URL. If you need to manually edit them:

**k8s/backend-deployment.yaml**:
```yaml
image: DOCKER_REGISTRY_PLACEHOLDER/idurar-backend:latest  # Will be updated by pipeline
```

**k8s/frontend-deployment.yaml**:
```yaml
image: DOCKER_REGISTRY_PLACEHOLDER/idurar-frontend:latest  # Will be updated by pipeline
```

The Jenkins pipeline automatically updates these placeholders during deployment.

### Step 3: Configure Kubernetes Namespace

The pipeline uses the namespace `idurar-crm` by default. To change it, update the `NAMESPACE` variable in the Jenkinsfile:

```groovy
NAMESPACE = 'your-namespace-name'
```

### Step 4: Set Up MongoDB Authentication (Strongly Recommended for Production)

For production environments, MongoDB should always be secured with authentication. For development/testing, you can skip this step.

**Create MongoDB Secret:**

```bash
kubectl create secret generic mongodb-secret \
  --from-literal=username=admin \
  --from-literal=password=your-secure-password \
  -n idurar-crm
```

Or use the provided template:

```bash
cp k8s/mongodb-secret.yaml.example k8s/mongodb-secret.yaml
# Edit mongodb-secret.yaml with your credentials (base64 encoded)
kubectl apply -f k8s/mongodb-secret.yaml -n idurar-crm
```

**Important**: Never commit `*-secret.yaml` files to version control. They're already excluded in `.gitignore`.

**Update Backend Connection String:**

When MongoDB authentication is enabled, you must also update the backend to use authenticated connection. Use the backend secret template:

```bash
cp k8s/backend-secret.yaml.example k8s/backend-secret.yaml
# Edit backend-secret.yaml with your MongoDB credentials
kubectl apply -f k8s/backend-secret.yaml -n idurar-crm
```

Then update `k8s/backend-deployment.yaml` to use the secret (see comments in backend-secret.yaml.example).

### Step 5: Set Up Additional Backend Environment Variables (Optional)

For sensitive backend configuration like JWT secrets, create additional secrets:

```bash
kubectl create secret generic backend-secrets \
  --from-literal=JWT_SECRET=your-jwt-secret \
  --from-literal=SESSION_SECRET=your-session-secret \
  -n idurar-crm
```

Then update `k8s/backend-deployment.yaml` to reference it:

```yaml
envFrom:
  - configMapRef:
      name: idurar-config
  - secretRef:
      name: backend-secrets
```

## Creating a Jenkins Pipeline Job

1. Go to Jenkins Dashboard
2. Click "New Item"
3. Enter a name (e.g., "IDURAR-CRM-Pipeline")
4. Select "Pipeline" and click OK
5. Under "Pipeline" section:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your repository URL
   - Branch: */main (or your branch name)
   - Script Path: Jenkinsfile
6. Click "Save"

## Running the Pipeline

### Manual Trigger
1. Go to your pipeline job
2. Click "Build Now"
3. Monitor the progress in the Console Output

### Automatic Trigger
Set up webhooks in your Git repository to trigger builds automatically on push:

1. In Jenkins job configuration, enable "GitHub hook trigger for GITScm polling" (for GitHub)
2. Add webhook in your repository settings pointing to: `http://your-jenkins-url/github-webhook/`

## Pipeline Stages Explained

### 1. Checkout Stage
Checks out the source code from the repository.

### 2. Build Stage
- **Backend Build**: Installs npm dependencies for the backend
- **Frontend Build**: Installs dependencies and builds the React application
- Both run in parallel for faster execution

### 3. Automated Tests Stage
- **Backend Tests**: Validates backend structure and dependencies
- **Frontend Tests**: Checks build output and runs linter if available
- Runs in parallel

### 4. Docker Build & Push Stage
- Builds Docker images for both frontend and backend
- Tags images with build number and 'latest'
- Pushes images to the configured Docker registry
- Runs in parallel

### 5. Deploy to Kubernetes Stage
- Creates namespace if it doesn't exist
- Applies all Kubernetes manifests from `k8s/` directory
- Updates deployments with new image versions
- Waits for rollout to complete
- Displays deployment status

## Kubernetes Architecture

The application deploys with the following components:

- **MongoDB**: Stateful database with persistent volume
- **Backend**: 2 replicas of Node.js API (ClusterIP service)
- **Frontend**: 2 replicas of React app (LoadBalancer service)

Services:
- `mongodb-service:27017` - Internal MongoDB access
- `backend-service:8888` - Internal API access
- `frontend-service:80` - External web access (LoadBalancer)

## Troubleshooting

### Pipeline Fails at Docker Build
- Ensure Docker daemon is running on Jenkins agent
- Verify Docker credentials are correct
- Check if Jenkins user has Docker permissions: `sudo usermod -aG docker jenkins`

### Pipeline Fails at Kubernetes Deploy
- Verify kubeconfig file is valid and has proper permissions
- Check if namespace exists: `kubectl get namespace`
- Verify kubectl is installed: `kubectl version --client`

### Images Not Updating in Kubernetes
- Check if image pull policy is set correctly
- Verify image names match in deployment files
- Try: `kubectl rollout restart deployment/idurar-backend -n idurar-crm`

### Build Fails with Node.js Errors
- Ensure correct Node.js version (20.9.0) is installed
- Check npm version (10.2.4)
- Clear npm cache: `npm cache clean --force`

## Monitoring Deployment

After successful deployment, check the status:

```bash
# Get pods status
kubectl get pods -n idurar-crm

# Get services
kubectl get services -n idurar-crm

# View logs
kubectl logs -f deployment/idurar-backend -n idurar-crm
kubectl logs -f deployment/idurar-frontend -n idurar-crm

# Get external IP (for frontend LoadBalancer)
kubectl get service frontend-service -n idurar-crm
```

## Customization

### Adding Real Tests

When you add test frameworks (Jest, Mocha, etc.), update the test stages:

**Backend Tests**:
```groovy
stage('Backend Tests') {
    steps {
        dir('backend') {
            sh 'npm test'
        }
    }
}
```

**Frontend Tests**:
```groovy
stage('Frontend Tests') {
    steps {
        dir('frontend') {
            sh 'npm test'
        }
    }
}
```

### Deploying to Staging First

Add a staging deployment stage before production:

```groovy
stage('Deploy to Staging') {
    steps {
        sh '''
            kubectl apply -f k8s/ -n idurar-staging
            kubectl set image deployment/idurar-backend backend=${BACKEND_IMAGE}:${IMAGE_TAG} -n idurar-staging
            kubectl set image deployment/idurar-frontend frontend=${FRONTEND_IMAGE}:${IMAGE_TAG} -n idurar-staging
        '''
    }
}

stage('Approval') {
    steps {
        input message: 'Deploy to Production?', ok: 'Deploy'
    }
}

stage('Deploy to Production') {
    steps {
        // Production deployment steps
    }
}
```

## Security Best Practices

1. **Never commit credentials** in the Jenkinsfile or code
2. Use **Kubernetes Secrets** for sensitive environment variables
3. Enable **RBAC** in Kubernetes for fine-grained access control
4. Use **private Docker registry** for production images
5. Implement **image scanning** before deployment
6. Set up **network policies** in Kubernetes
7. Use **SSL/TLS** for all external endpoints

## Support

For issues related to:
- **IDURAR Application**: Check the main [README.md](README.md)
- **Jenkins Setup**: Visit [Jenkins Documentation](https://www.jenkins.io/doc/)
- **Kubernetes**: Visit [Kubernetes Documentation](https://kubernetes.io/docs/)
- **Docker**: Visit [Docker Documentation](https://docs.docker.com/)
