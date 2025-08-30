pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'junaiddocker743/greenx-app'
        DEPLOY_HOST = '192.168.18.116'
    }

    triggers {
        githubPush()  // Webhook trigger
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Lint') {
            steps {
                echo '🔍 Running flake8 lint checks...'
                sh '''
                    pip install flake8 || true
                    flake8 --ignore=E501 ./GreenX_DCS_Assesment_Tool_Backend || true
                '''
            }
        }

        stage('Build Images') {
            steps {
                echo '🐳 Building Docker images...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}-backend:latest ./GreenX_DCS_Assesment_Tool_Backend
                    docker build -t ${DOCKER_IMAGE}-frontend:latest ./greenX-assessment-tool-frontend
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '📦 Pushing images to DockerHub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}-backend:latest
                        docker push ${DOCKER_IMAGE}-frontend:latest
                    '''
                }
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                echo '🚀 Deploying to remote server...'
                sshagent(['deploy-creds']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no deploy@${DEPLOY_HOST} "
                            docker pull ${DOCKER_IMAGE}-backend:latest &&
                            docker pull ${DOCKER_IMAGE}-frontend:latest &&
                            cd ~/greenx || git clone https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git greenx;
                            cd ~/greenx &&
                            git pull origin main &&
                            docker compose down || true &&
                            docker compose up -d &&
                            docker compose ps
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build + Push + Remote Deploy successful.'
            // Email notification on success
            mail to: 'hafizjunaidhussain4@gmail.com',
                 subject: "✅ Pipeline Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Deployment to remote server successful.\nCheck Jenkins for details: ${env.BUILD_URL}"
        }
        failure {
            echo '❌ Pipeline failed. Check logs.'
            // Email notification on failure
            mail to: 'hafizjunaidhussain4@gmail.com',
                 subject: "❌ Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The pipeline failed.\nCheck Jenkins for details: ${env.BUILD_URL}"
        }
    }
}

