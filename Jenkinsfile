pipeline {
    agent any

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
                sh 'echo "Running Lint..."'
                // Example: sh 'eslint .'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building application..."'
                // Example for Node.js: sh 'npm install && npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running Tests..."'
                // Example: sh 'npm test'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t myapp:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploying to server..."'
                // yahan aap ssh ya docker run use kar sakte ho
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

