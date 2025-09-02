pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        DEPLOY_USER = 'root'
        DEPLOY_HOST = '192.168.18.116'
        DEPLOY_PATH = '/root/project'
    }

    stages {
        stage('Clone Code from GitHub') {
            steps {
                retry(3) {
                    sh 'git config --global http.postBuffer 524288000'
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git']],
                        extensions: [[$class: 'CloneOption', shallow: true, depth: 1, timeout: 10]]
                    ])
                }
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

        stage('Copy Project to Deployment Server') {
            steps {
                sh """
                    echo "📂 Copying only deploy compose file to remote server..."
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'

                    rsync -avz docker-compose.deploy.yml \
                        ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                """
            }
        }

        stage('Deploy on Remote Server') {
            steps {
                sh """
                    echo "🚀 Deploying on remote server..."
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                        cd ${DEPLOY_PATH} &&
                        docker compose -f docker-compose.deploy.yml up -d
                    '
                """
            }
        }
    }
}

