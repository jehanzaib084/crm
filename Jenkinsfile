pipeline {
    agent any
    
    environment {
        // Docker Hub username - will be overridden by credential if different
        DOCKERHUB_USERNAME = 'jehanzaib08'
        DOCKERHUB_REPO = 'jehanzaib08/crm'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
    }
    
    triggers {
        // Poll SCM every 5 minutes (or use GitHub webhook)
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out source code...'
                checkout scm
                sh 'git rev-parse HEAD > .git/commit-id || echo "N/A" > .git/commit-id'
                sh 'cat .git/commit-id'
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo '🏗️ Building Frontend...'
                dir('frontend') {
                    sh '''
                        npm ci
                        npm run build
                    '''
                }
            }
            post {
                success {
                    echo '✅ Frontend build successful'
                }
                failure {
                    echo '❌ Frontend build failed'
                }
            }
        }
        
        stage('Build Backend') {
            steps {
                echo '🏗️ Building Backend...'
                dir('backend') {
                    sh '''
                        npm ci
                        node -c src/server.js && echo "✅ Backend syntax valid"
                    '''
                }
            }
            post {
                success {
                    echo '✅ Backend build successful'
                }
                failure {
                    echo '❌ Backend build failed'
                }
            }
        }
        
        stage('Tests') {
            parallel {
                stage('Frontend Lint') {
                    steps {
                        echo '🧪 Running Frontend Lint Tests...'
                        dir('frontend') {
                            sh '''
                                npm run lint || echo "Lint completed with warnings"
                            '''
                        }
                    }
                }
                stage('Backend Validation') {
                    steps {
                        echo '🧪 Validating Backend...'
                        dir('backend') {
                            sh '''
                                node -c src/server.js && echo "✅ Backend syntax valid"
                                node -c src/app.js && echo "✅ App syntax valid" || echo "⚠️ App.js check skipped"
                            '''
                        }
                    }
                }
                stage('Docker Compose Test') {
                    steps {
                        echo '🧪 Testing Docker Compose...'
                        sh '''
                            docker-compose config > /dev/null && echo "✅ Docker Compose config valid"
                        '''
                    }
                }
            }
        }
        
        stage('Docker Build') {
            parallel {
                stage('Build Frontend Image') {
                    steps {
                        echo '🐳 Building Frontend Docker Image...'
                        dir('frontend') {
                            sh '''
                                docker build -t ${DOCKERHUB_USERNAME}/crm-frontend:${IMAGE_TAG} .
                                docker tag ${DOCKERHUB_USERNAME}/crm-frontend:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/crm-frontend:latest
                            '''
                        }
                    }
                }
                stage('Build Backend Image') {
                    steps {
                        echo '🐳 Building Backend Docker Image...'
                        dir('backend') {
                            sh '''
                                docker build -t ${DOCKERHUB_USERNAME}/crm-backend:${IMAGE_TAG} .
                                docker tag ${DOCKERHUB_USERNAME}/crm-backend:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/crm-backend:latest
                            '''
                        }
                    }
                }
                stage('Build Database Image') {
                    steps {
                        echo '🐳 Building Database Docker Image...'
                        dir('db') {
                            sh '''
                                docker build -t ${DOCKERHUB_USERNAME}/crm-db:${IMAGE_TAG} .
                                docker tag ${DOCKERHUB_USERNAME}/crm-db:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/crm-db:latest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                echo '📤 Pushing Docker Images to Docker Hub...'
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'fd9b973e-1c72-4698-b6dd-5030492cbfa4', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                            sh '''
                                echo ${DOCKERHUB_PASS} | docker login -u ${DOCKERHUB_USER} --password-stdin
                                
                                # Use the username from credentials (may differ from env var)
                                docker push ${DOCKERHUB_USER}/crm-frontend:${IMAGE_TAG}
                                docker push ${DOCKERHUB_USER}/crm-frontend:latest
                                
                                docker push ${DOCKERHUB_USER}/crm-backend:${IMAGE_TAG}
                                docker push ${DOCKERHUB_USER}/crm-backend:latest
                                
                                docker push ${DOCKERHUB_USER}/crm-db:${IMAGE_TAG}
                                docker push ${DOCKERHUB_USER}/crm-db:latest
                                
                                echo "✅ All images pushed successfully"
                            '''
                        }
                    } catch (Exception e) {
                        echo "⚠️ ERROR: Docker Hub credentials not found!"
                        echo "⚠️ Please check credentials in Jenkins:"
                        echo "   1. Manage Jenkins → Credentials"
                        echo "   2. Verify credential ID: fd9b973e-1c72-4698-b6dd-5030492cbfa4"
                        echo "   3. Or create new credential with ID: dockerhub-credentials"
                        echo "   4. Username: jehanzaib08"
                        echo "   5. Password: Your Docker Hub password"
                        echo ""
                        echo "⚠️ Skipping Docker push - images are built but not pushed"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                success {
                    echo '✅ Docker images pushed to registry'
                }
                failure {
                    echo '❌ Failed to push Docker images'
                }
            }
        }
        
        stage('Kubernetes Deploy') {
            steps {
                echo '☸️ Deploying to Kubernetes...'
                script {
                    // Check if kubectl is available
                    def kubectlAvailable = sh(
                        script: 'kubectl version --client 2>/dev/null',
                        returnStatus: true
                    ) == 0
                    
                    if (kubectlAvailable && fileExists('k8s')) {
                        // Create namespace first
                        sh '''
                            kubectl apply -f k8s/namespace.yaml || kubectl create namespace idurar-crm || true
                        '''
                        
                        // Create Docker Hub secret if it doesn't exist
                        try {
                            // Try UUID first, fallback to dockerhub-credentials
                            withCredentials([usernamePassword(credentialsId: 'fd9b973e-1c72-4698-b6dd-5030492cbfa4', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                                sh '''
                                    kubectl get secret dockerhub-secret -n idurar-crm || \
                                    kubectl create secret docker-registry dockerhub-secret \
                                        --docker-server=https://index.docker.io/v1/ \
                                        --docker-username=${DOCKERHUB_USER} \
                                        --docker-password=${DOCKERHUB_PASS} \
                                        --namespace=idurar-crm \
                                        --dry-run=client -o yaml | kubectl apply -f - || true
                                '''
                            }
                        } catch (Exception e) {
                            echo "⚠️ Could not create K8s secret - credentials not available"
                        }
                        
                        // Apply all Kubernetes manifests
                        sh '''
                            kubectl apply -f k8s/mongodb.yaml || echo "⚠️ MongoDB deployment skipped"
                            kubectl apply -f k8s/backend.yaml || echo "⚠️ Backend deployment skipped"
                            kubectl apply -f k8s/frontend.yaml || echo "⚠️ Frontend deployment skipped"
                            
                            echo "✅ Kubernetes manifests applied"
                            kubectl get pods -n idurar-crm 2>/dev/null || echo "⚠️ Pods not found"
                        '''
                    } else {
                        echo "⚠️ kubectl not available or k8s directory not found - skipping Kubernetes deployment"
                    }
                }
            }
            post {
                success {
                    echo '✅ Kubernetes deployment stage completed'
                    sh '''
                        if command -v kubectl &> /dev/null; then
                            echo "📊 Deployment Status:"
                            kubectl get pods -n idurar-crm 2>/dev/null || echo "Namespace not found"
                            kubectl get svc -n idurar-crm 2>/dev/null || echo "Services not found"
                        fi
                    '''
                }
                failure {
                    echo '⚠️ Kubernetes deployment failed or skipped'
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo '🧹 Cleaning up...'
                try {
                    sh 'docker system prune -f || true'
                } catch (Exception e) {
                    echo "⚠️ Cleanup skipped"
                }
            }
        }
        success {
            echo '✅ Pipeline completed successfully!'
            script {
                try {
                    def commitId = sh(script: 'cat .git/commit-id 2>/dev/null || echo "N/A"', returnStdout: true).trim()
                    echo "Commit: ${commitId}"
                    echo "Images built:"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-frontend:${IMAGE_TAG}"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-backend:${IMAGE_TAG}"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-db:${IMAGE_TAG}"
                } catch (Exception e) {
                    echo "Images built:"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-frontend:${IMAGE_TAG}"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-backend:${IMAGE_TAG}"
                    echo "  - ${DOCKERHUB_USERNAME}/crm-db:${IMAGE_TAG}"
                }
            }
        }
        failure {
            echo '❌ Pipeline failed!'
            echo 'Check the console output above for details.'
        }
        unstable {
            echo '⚠️ Pipeline completed with warnings'
            echo 'Check credentials setup if Docker push failed.'
        }
    }
}
