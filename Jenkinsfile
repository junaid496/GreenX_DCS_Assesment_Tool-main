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

        stage('Wait for DB Ready') {
            steps {
                echo '⏳ Waiting for MySQL container to be ready...'
                sh '''
                    # Wait until MySQL is accepting connections
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
                    # Run migrations but continue even if already applied or error
                    docker exec -i ${COMPOSE_PROJECT_NAME}-backend-1 bash -c "cd /app && alembic upgrade head || true"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment & Migrations successful.'
            sh '${COMPOSE} ps'
        }
        failure {
            echo '❌ Build/Deploy/Migrations failed. Showing recent logs...'
            sh '${COMPOSE} logs --no-color --since 15m || true'
        }
        always {
            sh '${COMPOSE} logs --no-color --since 15m > compose-latest.log || true'
            archiveArtifacts artifacts: 'compose-latest.log', allowEmptyArchive: true
        }
    }
}


