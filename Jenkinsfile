pipeline {
    agent any

    environment {
        COMPOSE = 'docker compose'   // Agar system me sirf 'docker-compose' hai to yahan change kar do
        COMPOSE_PROJECT_NAME = 'greenx'
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

        stage('Verify Docker/Compose') {
            steps {
                sh '''
                    docker --version
                    ${COMPOSE} version
                '''
            }
        }

        stage('Build with Compose') {
            steps {
                sh '''
                    ${COMPOSE} build --pull
                '''
            }
        }

        stage('Deploy with Compose (Local Jenkins Server)') {
            steps {
                sh '''
                    ${COMPOSE} down || true
                    ${COMPOSE} up -d
                    ${COMPOSE} ps
                '''
            }
        }

        stage('Wait for DB Ready') {
            steps {
                echo '⏳ Waiting for MySQL container to be ready...'
                sh '''
                    until docker exec -i ${COMPOSE_PROJECT_NAME}-db-1 mysqladmin ping -h "127.0.0.1" --silent; do
                        echo "Waiting for database..."
                        sleep 5
                    done
                '''
            }
        }

        stage('Run Alembic Migrations') {
            steps {
                echo '🔹 Running backend migrations...'
                sh '''
                    docker exec -i ${COMPOSE_PROJECT_NAME}-backend-1 bash -c "cd /app && alembic upgrade head || true"
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '📦 Pushing images to DockerHub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        
                        # Backend image
                        docker build -t ${DOCKER_IMAGE}-backend:latest ./GreenX_DCS_Assesment_Tool_Backend
                        docker push ${DOCKER_IMAGE}-backend:latest
                        
                        # Frontend image
                        docker build -t ${DOCKER_IMAGE}-frontend:latest ./greenX-assessment-tool-frontend
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
            echo '✅ Deployment, Migrations & Push successful.'
            sh '${COMPOSE} ps'
            
            // Email notification on success
            mail to: 'hafizjunaidhussain4@gmail.com',
                 subject: "✅ Pipeline Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Deployment to local + remote successful.\nCheck Jenkins for details: ${env.BUILD_URL}"
        }
        failure {
            echo '❌ Build/Deploy/Migrations/Push failed. Showing recent logs...'
            sh '${COMPOSE} logs --no-color --since 15m || true'
            
            // Email notification on failure
            mail to: 'hafizjunaidhussain4@gmail.com',
                 subject: "❌ Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The pipeline failed.\nCheck Jenkins for details: ${env.BUILD_URL}"
        }
        always {
            sh '${COMPOSE} logs --no-color --since 15m > compose-latest.log || true'
            archiveArtifacts artifacts: 'compose-latest.log', allowEmptyArchive: true
        }
    }
}

