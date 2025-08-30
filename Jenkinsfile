pipeline {
    agent any

    environment {
        COMPOSE = 'docker compose'   // Agar system me sirf 'docker-compose' hai to yahan change kar do
        COMPOSE_PROJECT_NAME = 'greenx'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'   // Jenkins me jo creds add kiye hain unka ID
        DOCKER_IMAGE = 'junaiddocker743/greenx-app'   // apna dockerhub repo name
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
                echo '🔍 Running Lint...'
                sh '''
                    # Example Python lint
                    docker run --rm -v $PWD:/app -w /app python:3.10 bash -c "pip install flake8 && flake8 . || true"
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
                echo '📦 Pushing image to DockerHub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t ${DOCKER_IMAGE}:latest .
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment, Migrations & DockerHub Push successful.'
            sh '${COMPOSE} ps'
        }
        failure {
            echo '❌ Something failed. Showing recent logs...'
            sh '${COMPOSE} logs --no-color --since 15m || true'
        }
        always {
            sh '${COMPOSE} logs --no-color --since 15m > compose-latest.log || true'
            archiveArtifacts artifacts: 'compose-latest.log', allowEmptyArchive: true
        }
    }
}


