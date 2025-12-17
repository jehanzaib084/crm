# Quick Start: Jenkins CI/CD Setup

## ✅ What's Been Created

1. **Jenkinsfile** - Complete CI/CD pipeline with all required stages
2. **Kubernetes Manifests** - Ready-to-deploy K8s configurations
3. **Health Check Endpoint** - Added `/api/health` to backend

## 🚀 Quick Setup Steps

### 1. Jenkins Credentials (Required)

In Jenkins, go to **Manage Jenkins** → **Credentials** → **Add Credentials**:

**Docker Hub:**
- **Kind**: Username with password
- **ID**: `dockerhub-credentials`
- **Username**: `jehanzaib08`
- **Password**: Your Docker Hub password

### 2. Create Pipeline Job

1. **New Item** → Name: `idurar-crm-pipeline`
2. Select **Pipeline**
3. **Pipeline** section:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/jehanzaib084/crm.git`
   - **Branches**: `*/main` or `*/master`
   - **Script Path**: `Jenkinsfile`

### 3. GitHub Webhook (Optional but Recommended)

1. Go to: `https://github.com/jehanzaib084/crm/settings/hooks`
2. **Add webhook**:
   - **Payload URL**: `http://your-jenkins-url/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Just the push event

### 4. Run Pipeline

Click **Build Now** in Jenkins, or push to GitHub to trigger automatically.

## 📋 Pipeline Stages

✅ **Checkout** - Clones repository  
✅ **Build Frontend** - npm ci + build  
✅ **Build Backend** - npm ci + validation  
✅ **Tests** - Linting + validation  
✅ **Docker Build** - Builds 3 images (frontend, backend, db)  
✅ **Docker Push** - Pushes to Docker Hub  
✅ **Kubernetes Deploy** - Deploys to K8s (if configured)  

## 🐳 Docker Images

Images will be pushed to:
- `jehanzaib08/crm-frontend:latest` and `:BUILD_NUMBER`
- `jehanzaib08/crm-backend:latest` and `:BUILD_NUMBER`
- `jehanzaib08/crm-db:latest` and `:BUILD_NUMBER`

## ☸️ Kubernetes (Optional)

If you have a K8s cluster, the pipeline will automatically:
1. Create namespace `idurar-crm`
2. Create Docker Hub secret
3. Deploy MongoDB, Backend, and Frontend

## 📸 Screenshots for Submission

After running the pipeline, capture:
1. **Pipeline Stage View** - Shows all stages completed ✅
2. **Console Output** - Shows successful build logs
3. **Docker Hub** - Shows pushed images
4. **Kubernetes** - Shows deployed pods (if applicable)

## 🔧 Troubleshooting

**Build fails?**
- Check Node.js version (needs 20+)
- Verify Docker is running on Jenkins server
- Check Docker Hub credentials

**Push fails?**
- Verify Docker Hub credentials in Jenkins
- Check network connectivity
- Ensure Docker Hub account has push permissions

**K8s deploy fails?**
- Install kubectl on Jenkins server
- Configure kubeconfig credentials
- Or skip K8s stage if not needed

## 📝 Notes

- Pipeline triggers on **push** and **pull requests**
- Build timeout: 30 minutes
- Keeps last 10 builds
- All stages run in parallel where possible for speed

