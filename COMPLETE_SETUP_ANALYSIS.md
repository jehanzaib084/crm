# Complete Setup Analysis - Docker, Jenkins CI/CD, and Kubernetes

This document provides a comprehensive analysis of the entire containerization, CI/CD, and Kubernetes deployment setup for easy replication in other projects.

---

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Docker Setup](#docker-setup)
3. [Docker Compose](#docker-compose)
4. [Jenkins CI/CD Pipeline](#jenkins-cicd-pipeline)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Key Configuration Details](#key-configuration-details)
7. [Replication Guide](#replication-guide)

---

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   ├── .env (not in repo)
│   └── src/
│       ├── server.js
│       └── app.js (with /api/health endpoint)
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── db/
│   ├── Dockerfile
│   └── init-mongo.js
├── k8s/
│   ├── namespace.yaml
│   ├── mongodb.yaml
│   ├── backend.yaml
│   ├── frontend.yaml
│   └── dockerhub-secret.yaml (template)
├── docker-compose.yml
├── Jenkinsfile
└── .dockerignore (optional)
```

---

## 🐳 Docker Setup

### 1. Backend Dockerfile (`backend/Dockerfile`)

**Purpose:** Node.js/Express API server

**Key Features:**
- Uses `node:20-alpine` (lightweight)
- Installs dependencies with `npm ci` (clean install)
- Exposes port 8888
- Runs `node src/server.js`

**Template:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source
COPY . .

# Expose backend port
EXPOSE 8888

# Start the backend server
CMD ["node", "src/server.js"]
```

**Important Notes:**
- Uses `npm ci` for reproducible builds
- No multi-stage build needed (simple Node.js app)
- Ensure `src/server.js` exists and is the entry point

---

### 2. Frontend Dockerfile (`frontend/Dockerfile`)

**Purpose:** React/Vite application with Nginx

**Key Features:**
- **Multi-stage build:**
  - Stage 1: Build React app with Vite
  - Stage 2: Serve with Nginx
- Sets `VITE_BACKEND_SERVER=/` environment variable
- Configures Nginx to proxy `/api` requests to backend
- Serves static files and handles SPA routing

**Template:**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source
COPY . .

# Build the React application
# Set VITE_BACKEND_SERVER to root since nginx proxies /api to backend
ENV VITE_BACKEND_SERVER=/
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Configure nginx for API proxy
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    location /api { \
        proxy_pass http://backend:8888; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Important Notes:**
- `VITE_BACKEND_SERVER=/` is set because the frontend code adds `api/` prefix
- Nginx proxies `/api/*` to `http://backend:8888`
- `try_files` handles SPA routing (all routes serve `index.html`)
- Backend service name must match Docker Compose service name

---

### 3. Database Dockerfile (`db/Dockerfile`)

**Purpose:** MongoDB database with initialization

**Key Features:**
- Uses official `mongo:7.0` image
- Copies initialization script to `/docker-entrypoint-initdb.d/`
- Creates data directory
- Exposes port 27017

**Template:**
```dockerfile
FROM mongo:7.0

# Copy initialization script
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Create data directory
RUN mkdir -p /data/db

# Expose MongoDB port
EXPOSE 27017

# Set default command
CMD ["mongod"]
```

**Initialization Script (`db/init-mongo.js`):**
```javascript
// MongoDB initialization script
db = db.getSiblingDB('idurar');

// Create collections (they will be created automatically when data is inserted)
db.createCollection('admins');
db.createCollection('adminpasswords');
db.createCollection('settings');
// ... other collections

print('MongoDB initialized for IDURAR ERP/CRM');
```

**Important Notes:**
- Scripts in `/docker-entrypoint-initdb.d/` run only on first initialization
- Use `db.getSiblingDB()` to switch databases
- Collections are created automatically on first insert

---

## 🐙 Docker Compose

**File:** `docker-compose.yml`

**Purpose:** Orchestrates all services for local development

**Key Features:**
- Defines 3 services: db, backend, frontend
- Creates shared network
- Persistent volume for MongoDB data
- Health checks for MongoDB
- Environment variable configuration

**Template:**
```yaml
version: "3.9"

services:
  # MongoDB Database
  db:
    build:
      context: ./db
      dockerfile: Dockerfile
    container_name: idurar-mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongodb-data:/data/db
      - ./db/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - idurar-network
    environment:
      MONGO_INITDB_DATABASE: idurar
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s

  # Backend API (Node.js/Express)
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: idurar-backend
    restart: unless-stopped
    ports:
      - "8888:8888"
    env_file:
      - ./backend/.env
    environment:
      - DATABASE=mongodb://db:27017/idurar
      - PORT=8888
      - NODE_ENV=production
    depends_on:
      - db
    networks:
      - idurar-network

  # Frontend (React/Vite)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: idurar-frontend
    restart: unless-stopped
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - idurar-network

networks:
  idurar-network:
    driver: bridge

volumes:
  mongodb-data:
    driver: local
```

**Important Notes:**
- Service names (`db`, `backend`, `frontend`) are used for DNS resolution
- Backend connects to MongoDB using `mongodb://db:27017/idurar`
- Frontend Nginx proxies to `http://backend:8888`
- Health check ensures MongoDB is ready before backend starts

---

## 🔄 Jenkins CI/CD Pipeline

**File:** `Jenkinsfile`

**Purpose:** Automated build, test, Docker image creation, push to registry, and Kubernetes deployment

### Pipeline Stages:

1. **Checkout** - Clones repository
2. **Build Frontend** - `npm ci` + `npm run build`
3. **Build Backend** - `npm ci` + syntax validation
4. **Tests** (Parallel):
   - Frontend linting
   - Backend validation
   - Docker Compose validation
5. **Docker Build** (Parallel):
   - Build frontend image
   - Build backend image
   - Build database image
6. **Docker Push** - Push to Docker Hub
7. **Kubernetes Deploy** - Deploy to AKS

### Key Configuration:

**Environment Variables:**
```groovy
environment {
    DOCKERHUB_USERNAME = 'jehanzaib08'
    DOCKERHUB_REPO = 'jehanzaib08/crm'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
}
```

**Credentials Required:**
1. **Docker Hub:** `fd9b973e-1c72-4698-b6dd-5030492cbfa4`
   - Type: Username with password
   - Username: Docker Hub username (lowercase)
   - Password: Docker Hub password/token

2. **Kubernetes:** `2f2b05cf-882d-4e0a-8393-18f5ef3e75ee`
   - Type: Secret file
   - Content: kubeconfig file

**Docker Push Logic:**
- Normalizes username to lowercase (Docker Hub requirement)
- Pushes both `:BUILD_NUMBER` and `:latest` tags
- Handles credential errors gracefully

**Kubernetes Deploy Logic:**
- Loads kubeconfig from credentials
- Verifies cluster access
- Creates namespace
- Creates Docker Hub secret for image pulling
- Applies all manifests
- Shows external IP/hostname for frontend

### Customization Points:

1. **Change Docker Hub username:** Update `DOCKERHUB_USERNAME` in environment
2. **Change credential IDs:** Update `credentialsId` in `withCredentials` blocks
3. **Change namespace:** Update `idurar-crm` to your namespace
4. **Change image names:** Update `crm-frontend`, `crm-backend`, `crm-db` to your names

---

## ☸️ Kubernetes Deployment

### 1. Namespace (`k8s/namespace.yaml`)

**Purpose:** Isolates resources

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: idurar-crm
  labels:
    name: idurar-crm
    app: idurar-erp-crm
```

---

### 2. MongoDB (`k8s/mongodb.yaml`)

**Components:**
- PersistentVolumeClaim (5Gi storage)
- Deployment (1 replica)
- Service (ClusterIP)

**Key Features:**
- Persistent storage for data
- Health probes (liveness + readiness)
- Environment variable for database name

**Template:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
  namespace: idurar-crm
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb
  namespace: idurar-crm
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: mongodb
        image: jehanzaib08/crm-db:latest
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_DATABASE
          value: "idurar"
        volumeMounts:
        - name: mongodb-data
          mountPath: /data/db
        livenessProbe:
          exec:
            command: ["mongosh", "--eval", "db.adminCommand('ping')"]
          initialDelaySeconds: 30
        readinessProbe:
          exec:
            command: ["mongosh", "--eval", "db.adminCommand('ping')"]
          initialDelaySeconds: 10
      volumes:
      - name: mongodb-data
        persistentVolumeClaim:
          claimName: mongodb-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  namespace: idurar-crm
spec:
  type: ClusterIP
  ports:
  - port: 27017
    targetPort: 27017
  selector:
    app: mongodb
```

---

### 3. Backend (`k8s/backend.yaml`)

**Components:**
- Deployment (2 replicas for high availability)
- Service (ClusterIP)

**Key Features:**
- Health endpoint: `/api/health`
- Resource limits
- Image pull secret for Docker Hub
- Environment variables for database connection

**Template:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: idurar-crm
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: backend
        image: jehanzaib08/crm-backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8888
        env:
        - name: DATABASE
          value: "mongodb://mongodb:27017/idurar"
        - name: PORT
          value: "8888"
        - name: NODE_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8888
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8888
          initialDelaySeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      imagePullSecrets:
      - name: dockerhub-secret

---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: idurar-crm
spec:
  type: ClusterIP
  ports:
  - port: 8888
    targetPort: 8888
  selector:
    app: backend
```

**Important:** Backend must have `/api/health` endpoint:
```javascript
// In backend/src/app.js
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});
```

---

### 4. Frontend (`k8s/frontend.yaml`)

**Components:**
- Deployment (2 replicas)
- Service (LoadBalancer with Azure annotations)

**Key Features:**
- LoadBalancer type for external access
- Azure DNS label annotation
- Resource limits

**Template:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: idurar-crm
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: frontend
        image: jehanzaib08/crm-frontend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: idurar-crm
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: /
    service.beta.kubernetes.io/azure-dns-label-name: idurar-crm
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: frontend
```

**Azure Annotations:**
- `azure-dns-label-name`: Creates DNS name (may not work in all regions)
- `azure-load-balancer-health-probe-request-path`: Health check path

---

## 🔑 Key Configuration Details

### Backend Health Endpoint

**Required:** `/api/health` endpoint for Kubernetes probes

```javascript
// backend/src/app.js
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});
```

### Frontend API Configuration

**Important:** Frontend Dockerfile sets `VITE_BACKEND_SERVER=/` because:
- Frontend code adds `api/` prefix automatically
- Nginx proxies `/api/*` to backend
- Final URL: `/api/...` → `http://backend:8888/api/...`

### Database Connection

**Docker Compose:** `mongodb://db:27017/idurar`
**Kubernetes:** `mongodb://mongodb:27017/idurar`

Service names must match!

### Image Naming Convention

- Frontend: `{username}/crm-frontend:latest`
- Backend: `{username}/crm-backend:latest`
- Database: `{username}/crm-db:latest`

---

## 📝 Replication Guide

### Step 1: Create Dockerfiles

1. **Backend Dockerfile:**
   - Copy template
   - Update `EXPOSE` port if different
   - Update `CMD` entry point if different

2. **Frontend Dockerfile:**
   - Copy template
   - Update `VITE_BACKEND_SERVER` if your frontend config differs
   - Update Nginx proxy target if backend service name differs

3. **Database Dockerfile:**
   - Copy template
   - Update initialization script for your database schema
   - Change MongoDB version if needed

### Step 2: Create Docker Compose

1. Copy template
2. Update service names
3. Update ports if needed
4. Update environment variables
5. Update database connection strings

### Step 3: Create Kubernetes Manifests

1. **Namespace:**
   - Update namespace name
   - Update labels

2. **MongoDB:**
   - Update image name
   - Update database name
   - Update storage size if needed

3. **Backend:**
   - Update image name
   - Update health endpoint path if different
   - Update resource limits
   - Update environment variables
   - Update database connection string

4. **Frontend:**
   - Update image name
   - Update Azure DNS label name
   - Update resource limits

### Step 4: Create Jenkinsfile

1. **Update Environment:**
   ```groovy
   DOCKERHUB_USERNAME = 'your-username'
   DOCKERHUB_REPO = 'your-username/your-repo'
   ```

2. **Update Credential IDs:**
   - Docker Hub: `credentialsId: 'your-dockerhub-credential-id'`
   - Kubernetes: `credentialsId: 'your-kubeconfig-credential-id'`

3. **Update Namespace:**
   - Replace `idurar-crm` with your namespace

4. **Update Image Names:**
   - Replace `crm-frontend`, `crm-backend`, `crm-db` with your names

5. **Update Build Commands:**
   - If using different package managers (yarn, pnpm), update commands
   - If different build scripts, update accordingly

### Step 5: Setup Jenkins Credentials

1. **Docker Hub:**
   - Type: Username with password
   - ID: Use UUID or descriptive name
   - Username: Your Docker Hub username (lowercase)
   - Password: Your Docker Hub password/token

2. **Kubernetes:**
   - Type: Secret file
   - ID: Use UUID or descriptive name
   - Content: Your kubeconfig file

### Step 6: Test Locally

```bash
# Build and run with Docker Compose
docker-compose up --build

# Test services
curl http://localhost:3000
curl http://localhost:8888/api/health
```

### Step 7: Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Check status
kubectl get pods -n your-namespace
kubectl get svc -n your-namespace
```

---

## 🎯 Quick Checklist for Replication

- [ ] Create 3 Dockerfiles (backend, frontend, db)
- [ ] Create docker-compose.yml
- [ ] Add health endpoint to backend (`/api/health`)
- [ ] Configure frontend API base URL
- [ ] Create k8s/ directory with 4 manifests
- [ ] Update all image names
- [ ] Update all service names
- [ ] Update namespace name
- [ ] Create Jenkinsfile
- [ ] Update Jenkinsfile credential IDs
- [ ] Update Jenkinsfile Docker Hub username
- [ ] Setup Jenkins credentials
- [ ] Test locally with docker-compose
- [ ] Test Kubernetes deployment
- [ ] Verify external IP/hostname

---

## 📚 Additional Resources

- **Docker Hub:** https://hub.docker.com
- **Kubernetes Docs:** https://kubernetes.io/docs/
- **Azure AKS:** https://docs.microsoft.com/azure/aks/
- **Jenkins Pipeline:** https://www.jenkins.io/doc/book/pipeline/

---

## 🔧 Troubleshooting

### Docker Build Fails
- Check Dockerfile syntax
- Verify base images exist
- Check build context paths

### Docker Push Fails
- Verify Docker Hub credentials
- Check username is lowercase
- Verify repository exists or allows auto-creation

### Kubernetes Deploy Fails
- Check kubeconfig is valid
- Verify namespace exists
- Check image pull secrets
- Verify health endpoints work

### Frontend Not Accessible
- Check LoadBalancer external IP
- Verify pods are running
- Check service selector matches pod labels
- Verify Nginx configuration

---

**Last Updated:** Based on working production setup
**Project:** IDURAR ERP/CRM
**Stack:** MERN (MongoDB, Express, React, Node.js)
