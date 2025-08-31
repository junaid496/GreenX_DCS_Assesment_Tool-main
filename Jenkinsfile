pipeline {
    agent any

    environment {
        DEPLOY_SERVER = '192.168.18.116'
        APP_DIR = '/home/deploy/greenx_app' // directory on deploy server
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Pull code from GitHub
                git branch: 'main', url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                // Build Docker images locally on Jenkins server using Docker Compose
                sh 'docker-compose -f docker-compose.yml build --no-cache'
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                // Copy all project files to deploy server
                sh "rsync -avz --delete ./ deploy@${DEPLOY_SERVER}:${APP_DIR}"

                // SSH into deploy server and run docker-compose
                sh """
                ssh deploy@${DEPLOY_SERVER} '
                    cd ${APP_DIR} &&
                    docker-compose down &&
                    docker-compose up -d --build
                '
                """
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
