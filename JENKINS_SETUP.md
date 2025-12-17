# Jenkins CI/CD Setup Guide

This guide will help you set up Jenkins for the IDURAR ERP/CRM project.

## Prerequisites

1. Jenkins installed and running
2. Docker installed on Jenkins server
3. Docker Hub account (username: `jehanzaib08`)
4. Kubernetes cluster access (optional, for deployment stage)
5. Required Jenkins plugins installed

## Required Jenkins Plugins

Install these plugins via Jenkins Plugin Manager:

- **Pipeline** (usually pre-installed)
- **Docker Pipeline**
- **Kubernetes** (if deploying to K8s)
- **GitHub Integration** (for webhooks)
- **Credentials Binding**

## Jenkins Credentials Setup

### 1. Docker Hub Credentials

1. Go to **Jenkins** → **Manage Jenkins** → **Credentials**
2. Click **Add Credentials**
3. Select **Username with password**
4. Fill in:
   - **ID**: `dockerhub-credentials`
   - **Username**: `jehanzaib08`
   - **Password**: Your Docker Hub password
   - **Description**: Docker Hub credentials for pushing images

### 2. Kubernetes Config (Optional)

If deploying to Kubernetes:

1. Go to **Jenkins** → **Manage Jenkins** → **Credentials**
2. Click **Add Credentials**
3. Select **Secret file** or **Secret text**
4. Fill in:
   - **ID**: `kubeconfig`
   - Upload your kubeconfig file or paste the content

## Creating the Jenkins Pipeline

### Method 1: Pipeline from SCM (Recommended)

1. Go to **Jenkins** → **New Item**
2. Enter name: `idurar-crm-pipeline`
3. Select **Pipeline**
4. Click **OK**
5. In **Pipeline** section:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/jehanzaib084/crm.git`
   - **Branches to build**: `*/main` or `*/master`
   - **Script Path**: `Jenkinsfile`
6. Click **Save**

### Method 2: Multibranch Pipeline

1. Go to **Jenkins** → **New Item**
2. Enter name: `idurar-crm-multibranch`
3. Select **Multibranch Pipeline**
4. Click **OK**
5. In **Branch Sources**:
   - Add source: **GitHub**
   - Repository URL: `https://github.com/jehanzaib084/crm.git`
   - Credentials: (if private repo)
6. In **Build Configuration**:
   - **Mode**: By Jenkinsfile
   - **Script Path**: `Jenkinsfile`
7. Click **Save**

## Pipeline Triggers

The Jenkinsfile is configured to trigger on:
- **GitHub Push** (via webhook)
- **Pull Requests** (if using multibranch pipeline)

### Setting up GitHub Webhook

1. Go to your GitHub repository: `https://github.com/jehanzaib084/crm`
2. Go to **Settings** → **Webhooks** → **Add webhook**
3. Fill in:
   - **Payload URL**: `x/`
   - **Content type**: `application/json`
   - **Events**: Select **Just the push event**
4. Click **Add webhook**

## Pipeline Stages

The pipeline includes:

1. **Checkout**: Clones the repository
2. **Build Frontend**: Installs dependencies and builds React app
3. **Build Backend**: Validates Node.js backend
4. **Tests**: 
   - Frontend linting
   - Backend validation
   - Docker Compose validation
5. **Docker Build**: Builds images for frontend, backend, and database
6. **Docker Push**: Pushes images to Docker Hub
7. **Kubernetes Deploy**: Deploys to Kubernetes cluster (if configured)

## Docker Images

The pipeline builds and pushes these images:

- `jehanzaib08/crm-frontend:latest` and `:BUILD_NUMBER`
- `jehanzaib08/crm-backend:latest` and `:BUILD_NUMBER`
- `jehanzaib08/crm-db:latest` and `:BUILD_NUMBER`

## Kubernetes Deployment

If you have a Kubernetes cluster:

1. Ensure `kubectl` is installed on Jenkins server
2. Configure kubeconfig credentials in Jenkins
3. The pipeline will automatically deploy using manifests in `k8s/` directory

### Manual Kubernetes Setup

```bash
# Create namespace
kubectl create namespace idurar-crm

# Create Docker Hub secret
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=jehanzaib08 \
  --docker-password=<YOUR_PASSWORD> \
  --docker-email=<YOUR_EMAIL> \
  --namespace=idurar-crm

# Apply manifests
kubectl apply -f k8s/
```

## Troubleshooting

### Docker Login Fails

- Verify Docker Hub credentials in Jenkins
- Check if Docker is running on Jenkins server
- Ensure Jenkins user has permission to use Docker

### Build Fails

- Check Node.js version (requires Node 20+)
- Verify all dependencies are in package.json
- Check build logs for specific errors

### Kubernetes Deploy Fails

- Verify kubectl is installed: `kubectl version --client`
- Check kubeconfig credentials
- Ensure cluster is accessible from Jenkins server

### Images Not Pushing

- Verify Docker Hub credentials
- Check network connectivity
- Ensure Docker Hub repository exists or allows auto-creation

## Testing the Pipeline

1. Make a small change to the repository
2. Commit and push to GitHub
3. The webhook should trigger Jenkins automatically
4. Or manually trigger: **Build Now** in Jenkins

## Viewing Pipeline Results

- **Blue Ocean**: Install Blue Ocean plugin for visual pipeline view
- **Console Output**: Click on build number → **Console Output**
- **Stage View**: See progress of each stage

## Next Steps

After successful pipeline setup:

1. Verify all stages complete successfully
2. Check Docker Hub for pushed images
3. Verify Kubernetes deployment (if configured)
4. Test the deployed application

## Support

For issues or questions:
- Check Jenkins console output for errors
- Verify all credentials are set correctly
- Ensure all required plugins are installed
