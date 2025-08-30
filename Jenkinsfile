pipeline {
    agent any

    environment {
        DEPLOY_HOST = '192.168.18.116'
    }

    triggers {
        githubPush() // GitHub webhook trigger
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
                echo '🔍 Running flake8 lint checks...'
                sh '''
                    pip install flake8 || true
                    flake8 --ignore=E501 ./GreenX_DCS_Assesment_Tool_Backend || true
                '''
            }
        }

        stage('Build Images') {
            steps {
                echo '🐳 Building Docker images...'

                // Backend Docker build
                sh 'docker build -t greenx-backend:latest ./GreenX_DCS_Assesment_Tool_Backend'

                // Frontend Docker build
                timeout(time: 15, unit: 'MINUTES') {
                    sh '''
                        cd ./greenX-assessment-tool-frontend
                        rm -rf node_modules package-lock.json || true
                        npm install --legacy-peer-deps
                        npm run build
                        cd ..
                        docker build -t greenx-frontend:latest ./greenX-assessment-tool-frontend
                    '''
                }
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                echo '🚀 Deploying to remote server...'
                sshagent(['deploy-creds']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no deploy@${DEPLOY_HOST} "
                            # Pull latest images from Jenkins server
                            docker save greenx-backend:latest | docker load
                            docker save greenx-frontend:latest | docker load

                            # Git clone/update fix
                            if [ -d ~/greenx/.git ]; then
                                cd ~/greenx && git reset --hard && git pull origin main
                            else
                                rm -rf ~/greenx
                                git clone https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git greenx
                                cd ~/greenx
                            fi &&

                            # Deployment using docker-compose
                            docker-compose down || true &&
                            docker-compose up -d &&
                            docker-compose ps
                        "
                    '''
                }
            }
        }
    }
}


