pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'junaiddocker743/greenx-app'
        DEPLOY_HOST = '192.168.18.116'
    }

    triggers {
        githubPush() // GitHub webhook se trigger
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Lint & Build Docker Images') {
            steps {
                echo '🔍 Linting backend and building Docker images...'
                sh '''
                    # Backend lint
                    pip install flake8 || true
                    flake8 --ignore=E501 ./GreenX_DCS_Assesment_Tool_Backend || true

                    # Build backend Docker image
                    docker build -t ${DOCKER_IMAGE}-backend:latest ./GreenX_DCS_Assesment_Tool_Backend

                    # Frontend Docker build
                    cd ./greenX-assessment-tool-frontend
                    rm -rf node_modules package-lock.json || true
                    npm install --legacy-peer-deps
                    npm run build
                    cd ..
                    docker build -t ${DOCKER_IMAGE}-frontend:latest ./greenX-assessment-tool-frontend
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                echo '📦 Pushing Docker images...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}-backend:latest
                        docker push ${DOCKER_IMAGE}-frontend:latest
                    '''
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                echo '🚀 Deploying on remote server...'
                sshagent(['deploy-creds']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no deploy@${DEPLOY_HOST} "
                            docker pull ${DOCKER_IMAGE}-backend:latest
                            docker pull ${DOCKER_IMAGE}-frontend:latest
                            cd ~/greenx || git clone https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git greenx
                            cd ~/greenx
                            docker-compose down || true
                            docker-compose up -d
                        "
                    '''
                }
            }
        }
    }

    post {
        success { echo '✅ Pipeline finished successfully.' }
        failure { echo '❌ Pipeline failed.' }
    }
}


