pipeline {
    agent any

    environment {
        DEPLOY_SERVER = '192.168.18.116'
        APP_DIR = '/home/deploy/greenx_app' // directory on deploy server
    }

    triggers {
        // Trigger pipeline via GitHub webhook
        githubPush()
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clean workspace to avoid old code/cache issues
                deleteDir()

                // Pull code from GitHub using credentials
                git branch: 'main',
                    url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Build Docker Images') {
            steps {
                // Build Docker images locally on Jenkins server using Docker Compose with no cache
                sh 'docker-compose -f docker-compose.yml build --no-cache'
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                // Copy all project files to deploy server
                sh "rsync -avz --delete ./ deploy@${DEPLOY_SERVER}:${APP_DIR}"

                // SSH into deploy server and restart Docker Compose stack
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

