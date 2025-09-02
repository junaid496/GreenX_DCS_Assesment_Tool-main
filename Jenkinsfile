pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        DEPLOY_USER = 'root'
        DEPLOY_HOST = '192.168.18.116'
        DEPLOY_PATH = '/root/project'
        STACK_NAME = 'greenx'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                sh '''
                    echo "🔨 Building Docker images..."
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                    docker compose -f docker-compose.yml build
                    docker compose -f docker-compose.yml push
                '''
            }
        }

        stage('Copy Deploy Compose File') {
            steps {
                sh """
                    echo "📂 Copying deploy compose file..."
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'
                    rsync -avz docker-compose.deploy.yml ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                """
            }
        }

        stage('Deploy on Swarm with Rolling Update') {
            steps {
                sh """
                    echo "🚀 Deploying with rolling update..."
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                        cd ${DEPLOY_PATH} &&
                        docker stack deploy -c docker-compose.deploy.yml ${STACK_NAME}
                    '
                """
            }
        }
    }
}


