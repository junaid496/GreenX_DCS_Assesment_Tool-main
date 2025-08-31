pipeline {
    agent any

    environment {
        DB_URL = "mysql+pymysql://root:dbpasswd@db:3306/all_tables"
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
                        userRemoteConfigs: [[url: 'https://github.com/rizwan7161/jenkins.git']],
                        extensions: [[$class: 'CloneOption', shallow: true, depth: 1, timeout: 10]]
                    ])
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Copy Project to Deployment Server') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'
                    scp -o StrictHostKeyChecking=no -r * ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                """
            }
        }

        stage('Deploy on Remote Server') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                        cd ${DEPLOY_PATH} &&
                        mkdir -p data/db data/backend data/frontend &&
                        docker compose down || true &&
                        docker compose up --build -d
                    '
                """
            }
        }
    }
}



