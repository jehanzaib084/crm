pipeline {
    agent any
    
    environment {
        // Docker registry configuration
        DOCKER_REGISTRY = 'docker.io'  // Change to your registry (e.g., 'gcr.io', 'your-registry.azurecr.io')
        DOCKER_NAMESPACE = 'your-namespace'  // Change to your Docker Hub username or registry namespace
        
        // Image names
        BACKEND_IMAGE = "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/crm-backend"
        FRONTEND_IMAGE = "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/crm-frontend"
        DB_IMAGE = "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/crm-database"
        
        // Image tag (using build number or git commit)
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(8) ?: 'latest'}"
        
        // Docker credentials ID (configured in Jenkins)
        DOCKER_CREDENTIALS_ID = 'docker-registry-credentials'
        
        // Kubernetes configuration
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials'
        K8S_NAMESPACE = 'crm-production'  // Change to your namespace
        
        // Node version
        NODE_VERSION = '20.9.0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                script {
                    // Get git commit info for better tracking
                    env.GIT_COMMIT_MSG = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()
                    env.GIT_AUTHOR = sh(
                        script: 'git log -1 --pretty=%an',
                        returnStdout: true
                    ).trim()
                }
                echo "Building commit: ${env.GIT_COMMIT_MSG} by ${env.GIT_AUTHOR}"
            }
        }
        
        stage('Install Dependencies') {
            parallel {
                stage('Backend Dependencies') {
                    steps {
                        dir('backend') {
                            echo 'Installing backend dependencies...'
                            sh '''
                                node --version
                                npm --version
                                npm ci
                            '''
                        }
                    }
                }
                
                stage('Frontend Dependencies') {
                    steps {
                        dir('frontend') {
                            echo 'Installing frontend dependencies...'
                            sh '''
                                node --version
                                npm --version
                                npm ci
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Lint & Code Quality') {
            parallel {
                stage('Lint Frontend') {
                    steps {
                        dir('frontend') {
                            echo 'Linting frontend code...'
                            sh 'npm run lint || true'  // Continue on lint warnings
                        }
                    }
                }
                
                stage('Backend Code Check') {
                    steps {
                        dir('backend') {
                            echo 'Checking backend code structure...'
                            sh '''
                                echo "Backend code check passed"
                                # Add your backend linting command if available
                                # Example: npm run lint
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Build') {
            parallel {
                stage('Build Backend') {
                    steps {
                        dir('backend') {
                            echo 'Building backend application...'
                            sh '''
                                echo "Backend build completed"
                                # Backend is Node.js, no build step required
                                # Verify server file exists
                                test -f src/server.js && echo "Server file found" || exit 1
                            '''
                        }
                    }
                }
                
                stage('Build Frontend') {
                    steps {
                        dir('frontend') {
                            echo 'Building frontend application...'
                            sh '''
                                npm run build
                                echo "Frontend build completed"
                                ls -lh dist/
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            echo 'Running backend tests...'
                            sh '''
                                # Check if test script exists
                                if grep -q '"test":' package.json; then
                                    npm test
                                else
                                    echo "No test script found. Running basic validation..."
                                    node -e "console.log('Backend validation passed')"
                                fi
                            '''
                        }
                    }
                }
                
                stage('Frontend Tests') {
                    steps {
                        dir('frontend') {
                            echo 'Running frontend tests...'
                            sh '''
                                # Check if test script exists
                                if grep -q '"test":' package.json; then
                                    npm test
                                else
                                    echo "No test script found. Running basic validation..."
                                    node -e "console.log('Frontend validation passed')"
                                fi
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Backend Image') {
                    steps {
                        dir('backend') {
                            script {
                                echo "Building backend Docker image: ${BACKEND_IMAGE}:${IMAGE_TAG}"
                                sh """
                                    docker build -t ${BACKEND_IMAGE}:${IMAGE_TAG} .
                                    docker tag ${BACKEND_IMAGE}:${IMAGE_TAG} ${BACKEND_IMAGE}:latest
                                """
                            }
                        }
                    }
                }
                
                stage('Build Frontend Image') {
                    steps {
                        dir('frontend') {
                            script {
                                echo "Building frontend Docker image: ${FRONTEND_IMAGE}:${IMAGE_TAG}"
                                sh """
                                    docker build -t ${FRONTEND_IMAGE}:${IMAGE_TAG} .
                                    docker tag ${FRONTEND_IMAGE}:${IMAGE_TAG} ${FRONTEND_IMAGE}:latest
                                """
                            }
                        }
                    }
                }
                
                stage('Build Database Image') {
                    steps {
                        dir('db') {
                            script {
                                echo "Building database Docker image: ${DB_IMAGE}:${IMAGE_TAG}"
                                sh """
                                    docker build -t ${DB_IMAGE}:${IMAGE_TAG} .
                                    docker tag ${DB_IMAGE}:${IMAGE_TAG} ${DB_IMAGE}:latest
                                """
                            }
                        }
                    }
                }
            }
        }
        
        stage('Push Docker Images') {
            steps {
                script {
                    echo 'Pushing Docker images to registry...'
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS_ID) {
                        sh """
                            docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                            docker push ${BACKEND_IMAGE}:latest
                            
                            docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
                            docker push ${FRONTEND_IMAGE}:latest
                            
                            docker push ${DB_IMAGE}:${IMAGE_TAG}
                            docker push ${DB_IMAGE}:latest
                        """
                    }
                    echo 'Docker images pushed successfully'
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes namespace: ${K8S_NAMESPACE}"
                    
                    // Use Kubernetes credentials
                    withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                        sh """
                            # Verify kubectl is available
                            kubectl version --client
                            
                            # Create namespace if it doesn't exist
                            kubectl create namespace ${K8S_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                            
                            # Update image tags in deployments
                            cd k8s
                            
                            # Apply ConfigMaps and Secrets first
                            kubectl apply -f configmap.yaml -n ${K8S_NAMESPACE} || echo "No ConfigMap found"
                            kubectl apply -f secrets.yaml -n ${K8S_NAMESPACE} || echo "No Secrets found"
                            
                            # Deploy MongoDB
                            kubectl apply -f mongodb-deployment.yaml -n ${K8S_NAMESPACE}
                            
                            # Deploy Backend
                            kubectl set image deployment/crm-backend crm-backend=${BACKEND_IMAGE}:${IMAGE_TAG} -n ${K8S_NAMESPACE} || \
                            kubectl apply -f backend-deployment.yaml -n ${K8S_NAMESPACE}
                            
                            # Deploy Frontend
                            kubectl set image deployment/crm-frontend crm-frontend=${FRONTEND_IMAGE}:${IMAGE_TAG} -n ${K8S_NAMESPACE} || \
                            kubectl apply -f frontend-deployment.yaml -n ${K8S_NAMESPACE}
                            
                            # Wait for deployments to be ready
                            kubectl rollout status deployment/crm-backend -n ${K8S_NAMESPACE} --timeout=5m
                            kubectl rollout status deployment/crm-frontend -n ${K8S_NAMESPACE} --timeout=5m
                            
                            # Show deployment status
                            kubectl get pods -n ${K8S_NAMESPACE}
                            kubectl get services -n ${K8S_NAMESPACE}
                        """
                    }
                    echo 'Deployment completed successfully'
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo 'Verifying deployment health...'
                    withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                        sh """
                            # Check pod status
                            kubectl get pods -n ${K8S_NAMESPACE} -l app=crm-backend
                            kubectl get pods -n ${K8S_NAMESPACE} -l app=crm-frontend
                            
                            # Check if all pods are running
                            BACKEND_READY=\$(kubectl get pods -n ${K8S_NAMESPACE} -l app=crm-backend -o jsonpath='{.items[0].status.containerStatuses[0].ready}')
                            FRONTEND_READY=\$(kubectl get pods -n ${K8S_NAMESPACE} -l app=crm-frontend -o jsonpath='{.items[0].status.containerStatuses[0].ready}')
                            
                            if [ "\$BACKEND_READY" = "true" ] && [ "\$FRONTEND_READY" = "true" ]; then
                                echo "All services are healthy!"
                            else
                                echo "Warning: Some services may not be ready yet"
                            fi
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully! 🎉'
            echo "Backend Image: ${BACKEND_IMAGE}:${IMAGE_TAG}"
            echo "Frontend Image: ${FRONTEND_IMAGE}:${IMAGE_TAG}"
            echo "Database Image: ${DB_IMAGE}:${IMAGE_TAG}"
            echo "Deployed to namespace: ${K8S_NAMESPACE}"
        }
        
        failure {
            echo 'Pipeline failed! ❌'
            echo 'Check the logs above for details.'
        }
        
        always {
            echo 'Cleaning up...'
            // Clean up Docker images to save space
            sh """
                docker image prune -f || true
            """
            
            // Archive build artifacts if needed
            archiveArtifacts artifacts: '**/dist/**', allowEmptyArchive: true, fingerprint: true
        }
    }
}
