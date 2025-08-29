pipeline {
    agent any

    environment {
        COMPOSE = 'docker compose'   // Agar system me sirf 'docker-compose' hai to yahan change kar do
        COMPOSE_PROJECT_NAME = 'greenx'
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

        stage('Deploy with Compose') {
            steps {
                sh '''
                    ${COMPOSE} down || true
                    ${COMPOSE} up -d
                    ${COMPOSE} ps
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful.'
            sh '${COMPOSE} ps'
        }
        failure {
            echo '❌ Build/Deploy failed. Showing recent logs...'
            sh '${COMPOSE} logs --no-color --since 15m || true'
        }
        always {
            sh '${COMPOSE} logs --no-color --since 15m > compose-latest.log || true'
            archiveArtifacts artifacts: 'compose-latest.log', allowEmptyArchive: true
        }
    }
}


