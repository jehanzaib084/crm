# Quick Replication Template

Use this as a checklist when replicating the setup to another project.

## 🔄 Quick Copy-Paste Templates

### 1. Backend Dockerfile
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 8888
CMD ["node", "src/server.js"]
```

### 2. Frontend Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ENV VITE_BACKEND_SERVER=/
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } location /api { proxy_pass http://backend:8888; proxy_set_header Host $host; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Database Dockerfile
```dockerfile
FROM mongo:7.0
COPY init-mongo.js /docker-entrypoint-initdb.d/
RUN mkdir -p /data/db
EXPOSE 27017
CMD ["mongod"]
```

### 4. Backend Health Endpoint (REQUIRED)
Add to `backend/src/app.js`:
```javascript
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});
```

### 5. Jenkinsfile Key Sections

**Environment:**
```groovy
environment {
    DOCKERHUB_USERNAME = 'YOUR_USERNAME'
    DOCKERHUB_REPO = 'YOUR_USERNAME/YOUR_REPO'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
}
```

**Docker Push:**
```groovy
withCredentials([usernamePassword(credentialsId: 'YOUR_CREDENTIAL_ID', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
    sh '''
        DOCKER_USER_LOWER=$(echo "${DOCKERHUB_USER}" | tr '[:upper:]' '[:lower:]')
        echo ${DOCKERHUB_PASS} | docker login -u ${DOCKER_USER_LOWER} --password-stdin
        docker push ${DOCKER_USER_LOWER}/YOUR_FRONTEND:${IMAGE_TAG}
        docker push ${DOCKER_USER_LOWER}/YOUR_BACKEND:${IMAGE_TAG}
        docker push ${DOCKER_USER_LOWER}/YOUR_DB:${IMAGE_TAG}
    '''
}
```

**Kubernetes Deploy:**
```groovy
withCredentials([file(credentialsId: 'YOUR_KUBECONFIG_ID', variable: 'KUBECONFIG_FILE')]) {
    sh '''
        export KUBECONFIG=${KUBECONFIG_FILE}
        kubectl apply -f k8s/
    '''
}
```

## 📋 Replication Checklist

### Docker Setup
- [ ] Backend Dockerfile created
- [ ] Frontend Dockerfile created (multi-stage)
- [ ] Database Dockerfile created
- [ ] Health endpoint added to backend
- [ ] docker-compose.yml created
- [ ] Service names match across files

### Jenkins Setup
- [ ] Jenkinsfile created
- [ ] Docker Hub username updated
- [ ] Credential IDs updated
- [ ] Image names updated
- [ ] Namespace name updated

### Kubernetes Setup
- [ ] namespace.yaml created
- [ ] mongodb.yaml created (with PVC)
- [ ] backend.yaml created (with health probes)
- [ ] frontend.yaml created (with LoadBalancer)
- [ ] All image names updated
- [ ] All service names match

### Testing
- [ ] Local docker-compose works
- [ ] Images build successfully
- [ ] Jenkins pipeline runs
- [ ] Kubernetes deployment works
- [ ] External IP accessible

## 🔑 Key Values to Replace

| Current Value | Replace With |
|--------------|--------------|
| `idurar-crm` | Your namespace name |
| `jehanzaib08` | Your Docker Hub username |
| `crm-frontend` | Your frontend image name |
| `crm-backend` | Your backend image name |
| `crm-db` | Your database image name |
| `8888` | Your backend port (if different) |
| `idurar` | Your database name |
| `fd9b973e-1c72-4698-b6dd-5030492cbfa4` | Your Docker Hub credential ID |
| `2f2b05cf-882d-4e0a-8393-18f5ef3e75ee` | Your kubeconfig credential ID |

## 🚀 Quick Start Commands

```bash
# Local testing
docker-compose up --build

# Build images manually
docker build -t your-username/your-frontend:latest ./frontend
docker build -t your-username/your-backend:latest ./backend
docker build -t your-username/your-db:latest ./db

# Kubernetes deployment
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Check status
kubectl get pods -n your-namespace
kubectl get svc -n your-namespace
```
