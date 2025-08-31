pipeline {
    agent any

    environment {
        DEPLOY_HOST = '192.168.18.116'
        DEPLOY_PATH = '/root/project'
    }

    stages {
        stage('Clone Code from GitHub') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git']]
                ])
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Copy Project to Remote Server') {
            steps {
                sshagent(['ssh-root-key']) {
                    sh """
                        ssh root@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'
                        scp -r * root@${DEPLOY_HOST}:${DEPLOY_PATH}/
                    """
                }
            }
        }

        stage('Deploy on Remote Server') {
            steps {
                sshagent(['ssh-root-key']) {
                    sh """
                        ssh root@${DEPLOY_HOST} '
                            cd ${DEPLOY_PATH} &&
                            docker compose down || true &&
                            docker compose up --build -d
                        '
                    """
                }
            }
        }
    }
}


