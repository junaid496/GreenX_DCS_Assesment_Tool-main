pipeline {
    agent any

    triggers {
        githubPush()   // ✅ GitHub webhook trigger
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git',
                    branch: 'main',
                    credentialsId: 'github-creds'   // ✅ Aapka GitHub credentialsId
                )
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Running Build Step..."'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running Tests..."'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploy step (placeholder)"'
            }
        }
    }
}

