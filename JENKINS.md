# Jenkins Pipeline Documentation

This document describes the Jenkins CI/CD pipeline for the CRM application.

## Overview

The Jenkins pipeline automates the complete build, test, and deployment process for the CRM application, which consists of:

- **Frontend**: React/Vite application
- **Backend**: Node.js/Express API
- **Database**: MongoDB

## Pipeline Stages

### 1. Checkout
- Clones the repository
- Captures git commit information for tracking

### 2. Install Dependencies
- **Backend Dependencies**: Runs `npm ci` in the backend directory
- **Frontend Dependencies**: Runs `npm ci` in the frontend directory
- Runs in parallel for faster execution

### 3. Lint & Code Quality
- **Frontend**: Runs ESLint to check code quality
- **Backend**: Performs basic code structure checks
- Runs in parallel

### 4. Build
- **Backend**: Validates that all required files exist
- **Frontend**: Runs `npm run build` to create production build
- Runs in parallel

### 5. Test
- **Backend Tests**: Runs backend test suite if available
- **Frontend Tests**: Runs frontend test suite if available
- Falls back to basic validation if no tests are configured
- Runs in parallel

### 6. Build Docker Images
- **Backend Image**: Builds Docker image from `backend/Dockerfile`
- **Frontend Image**: Builds Docker image from `frontend/Dockerfile`
- **Database Image**: Builds Docker image from `db/Dockerfile`
- Tags images with both build-specific tag and `latest`
- Runs in parallel

### 7. Push Docker Images
- Pushes all images to the configured Docker registry
- Uses credentials stored in Jenkins

### 8. Deploy to Kubernetes
- Creates Kubernetes namespace if it doesn't exist
- Applies ConfigMaps and Secrets
- Deploys MongoDB, Backend, and Frontend
- Updates image tags in deployments
- Waits for deployments to be ready

### 9. Verify Deployment
- Checks pod status
- Verifies container health
- Reports deployment status

## Prerequisites

### Jenkins Configuration

1. **Jenkins Plugins Required**:
   - Docker Pipeline Plugin
   - Kubernetes Plugin
   - Git Plugin
   - Pipeline Plugin
   - Credentials Plugin

2. **Install Node.js**:
   - Install Node.js 20.9.0 on Jenkins agent
   - Or use Docker-based Jenkins agent with Node.js

3. **Install Docker**:
   - Docker must be available on Jenkins agent
   - Jenkins user must have permission to run Docker commands

4. **Install kubectl**:
   - Install kubectl on Jenkins agent
   - Ensure kubectl is in the PATH

### Credentials Setup

#### 1. Docker Registry Credentials

Create credentials in Jenkins:

```
Jenkins > Manage Jenkins > Credentials > Global > Add Credentials
```

- **Kind**: Username with password
- **ID**: `docker-registry-credentials`
- **Username**: Your Docker Hub username (or registry username)
- **Password**: Your Docker Hub password (or registry password/token)

For Docker Hub personal access token:
1. Go to Docker Hub > Account Settings > Security
2. Create a new access token
3. Use the token as the password

#### 2. Kubernetes Configuration

Create kubeconfig credential:

```
Jenkins > Manage Jenkins > Credentials > Global > Add Credentials
```

- **Kind**: Secret file
- **ID**: `kubeconfig-credentials`
- **File**: Upload your kubeconfig file

To get your kubeconfig:

```bash
# For most Kubernetes clusters
cat ~/.kube/config

# For cloud providers:
# AWS EKS
aws eks update-kubeconfig --name your-cluster-name --region us-east-1

# Google GKE
gcloud container clusters get-credentials your-cluster-name --region us-central1

# Azure AKS
az aks get-credentials --resource-group your-rg --name your-cluster-name
```

## Configuration

### Environment Variables

Edit the `Jenkinsfile` to configure these variables:

```groovy
environment {
    // Docker registry configuration
    DOCKER_REGISTRY = 'docker.io'  // Change to your registry
    DOCKER_NAMESPACE = 'your-namespace'  // Your Docker Hub username or registry namespace
    
    // Kubernetes configuration
    K8S_NAMESPACE = 'crm-production'  // Your Kubernetes namespace
    
    // Credentials IDs (must match Jenkins credentials)
    DOCKER_CREDENTIALS_ID = 'docker-registry-credentials'
    KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials'
}
```

### Docker Registry Options

#### Docker Hub
```groovy
DOCKER_REGISTRY = 'docker.io'
DOCKER_NAMESPACE = 'your-dockerhub-username'
```

#### Google Container Registry (GCR)
```groovy
DOCKER_REGISTRY = 'gcr.io'
DOCKER_NAMESPACE = 'your-project-id'
```

#### Amazon ECR
```groovy
DOCKER_REGISTRY = '123456789012.dkr.ecr.us-east-1.amazonaws.com'
DOCKER_NAMESPACE = 'your-app'
```

#### Azure Container Registry (ACR)
```groovy
DOCKER_REGISTRY = 'yourregistry.azurecr.io'
DOCKER_NAMESPACE = 'your-app'
```

#### Private Registry
```groovy
DOCKER_REGISTRY = 'registry.your-company.com'
DOCKER_NAMESPACE = 'your-namespace'
```

## Jenkins Job Setup

### Option 1: Pipeline Job from SCM

1. Create a new Pipeline job in Jenkins
2. In the job configuration:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your repository URL
   - **Branch Specifier**: `*/main` (or your branch)
   - **Script Path**: `Jenkinsfile`

### Option 2: Multibranch Pipeline

1. Create a new Multibranch Pipeline job
2. Configure branch source (GitHub, GitLab, Bitbucket, etc.)
3. Jenkins will automatically discover and build branches with a Jenkinsfile

### Option 3: GitHub Webhook (Automatic Builds)

1. In Jenkins job, enable "GitHub hook trigger for GITScm polling"
2. In GitHub repository settings:
   - Go to Settings > Webhooks
   - Add webhook: `http://your-jenkins-url/github-webhook/`
   - Content type: `application/json`
   - Events: "Just the push event"

## Running the Pipeline

### Manual Build

1. Go to your Jenkins job
2. Click "Build Now"
3. Monitor the build progress in the console output

### Automatic Build

- Commits to configured branches trigger automatic builds (if webhook is set up)
- The pipeline runs automatically on push

## Pipeline Parameters (Optional)

You can add parameters to the pipeline:

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['staging', 'production'], description: 'Deployment environment')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test stage')
        string(name: 'IMAGE_TAG', defaultValue: '', description: 'Custom image tag (leave empty for auto-generated)')
    }
    
    // ... rest of pipeline
}
```

## Monitoring and Debugging

### View Build Logs

1. Click on the build number
2. Click "Console Output"
3. View real-time logs

### Check Kubernetes Deployment

```bash
# Check pods
kubectl get pods -n crm-production

# View logs
kubectl logs -f deployment/crm-backend -n crm-production
kubectl logs -f deployment/crm-frontend -n crm-production

# Describe deployment
kubectl describe deployment crm-backend -n crm-production
```

### Common Issues

#### 1. Docker Build Fails

**Symptom**: Docker build stage fails

**Solutions**:
- Check Docker is installed and running on Jenkins agent
- Verify Jenkins user has Docker permissions: `sudo usermod -aG docker jenkins`
- Restart Jenkins after permission changes

#### 2. Docker Push Fails

**Symptom**: Cannot push images to registry

**Solutions**:
- Verify Docker registry credentials in Jenkins
- Check registry URL is correct
- Test manual login: `docker login <registry>`
- For ECR, ensure AWS credentials are configured

#### 3. Kubernetes Deployment Fails

**Symptom**: Cannot deploy to Kubernetes

**Solutions**:
- Verify kubeconfig credentials are correct
- Check namespace exists
- Verify cluster connectivity: `kubectl cluster-info`
- Check RBAC permissions

#### 4. Tests Fail

**Symptom**: Test stage fails

**Solutions**:
- Run tests locally first
- Check test dependencies are installed
- Review test logs in console output
- Ensure database is available for integration tests

## Kubernetes Setup

Before first deployment, set up Kubernetes resources:

```bash
# Create namespace
kubectl create namespace crm-production

# Create secrets (see k8s/README.md)
cp k8s/secrets.yaml.example k8s/secrets.yaml
# Edit secrets.yaml with your values
kubectl apply -f k8s/secrets.yaml -n crm-production

# Create Docker registry secret
kubectl create secret docker-registry docker-registry-secret \
  --docker-server=docker.io \
  --docker-username=your-username \
  --docker-password=your-password \
  --docker-email=your-email@example.com \
  -n crm-production

# Apply ConfigMaps
kubectl apply -f k8s/configmap.yaml -n crm-production
```

## Staging vs Production

To support multiple environments, you can:

1. **Use separate namespaces**:
```groovy
K8S_NAMESPACE = params.ENVIRONMENT == 'production' ? 'crm-production' : 'crm-staging'
```

2. **Use different branches**:
```groovy
K8S_NAMESPACE = env.BRANCH_NAME == 'main' ? 'crm-production' : 'crm-staging'
```

3. **Create separate Jenkins jobs** for each environment

## Security Best Practices

1. **Never commit secrets**: Always use Jenkins credentials
2. **Use least privilege**: Grant minimal permissions to service accounts
3. **Scan images**: Add container scanning stage
4. **RBAC**: Implement proper Kubernetes RBAC
5. **Network policies**: Restrict pod communication
6. **Secrets management**: Consider external secrets manager (Vault, AWS Secrets Manager)
7. **Image scanning**: Integrate vulnerability scanning (Trivy, Aqua)

## Advanced Features

### Email Notifications

Add to post section:

```groovy
post {
    failure {
        emailext (
            subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
            body: "Build failed. Check console output at ${env.BUILD_URL}",
            to: 'team@example.com'
        )
    }
}
```

### Slack Notifications

```groovy
post {
    success {
        slackSend channel: '#deployments', 
                  color: 'good', 
                  message: "Deployment successful: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
    }
}
```

### Approval Gate (for Production)

```groovy
stage('Approve Production Deploy') {
    when {
        branch 'main'
    }
    steps {
        input message: 'Deploy to production?', ok: 'Deploy'
    }
}
```

## Rollback Procedure

If deployment fails or issues are detected:

```bash
# Via Jenkins
# Re-run previous successful build

# Via kubectl
kubectl rollout undo deployment/crm-backend -n crm-production
kubectl rollout undo deployment/crm-frontend -n crm-production

# Or rollback to specific revision
kubectl rollout history deployment/crm-backend -n crm-production
kubectl rollout undo deployment/crm-backend --to-revision=3 -n crm-production
```

## Performance Optimization

1. **Use Docker layer caching**: Enable in Jenkins
2. **Parallel stages**: Already implemented for builds
3. **Incremental builds**: Skip unchanged stages
4. **Resource allocation**: Allocate sufficient resources to Jenkins agent

## Support

For issues or questions:
1. Check Jenkins console output
2. Review Kubernetes pod logs
3. Check this documentation
4. Contact DevOps team

## References

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Project README](./README.md)
- [Kubernetes Deployment Guide](./k8s/README.md)
