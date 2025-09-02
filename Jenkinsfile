pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        DEPLOY_USER = 'root'
        DEPLOY_HOST = '192.168.18.116'
        DEPLOY_PATH = '/root/project'
        ACTIVE_COLOR_FILE = "${DEPLOY_PATH}/active_color.txt"
    }

    stages {
        stage('Clone Code from GitHub') {
            steps {
                retry(3) {
                    sh 'git config --global http.postBuffer 524288000'
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/junaid496/GreenX_DCS_Assesment_Tool-main.git']],
                        extensions: [[$class: 'CloneOption', shallow: true, depth: 1, timeout: 10]]
                    ])
                }
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                sh '''
                    echo "🔨 Building Docker images..."
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                    docker compose -f docker-compose.yml build
                    docker compose -f docker-compose.yml push
                '''
            }
        }

        stage('Copy Project to Deployment Server') {
            steps {
                sh """
                    echo "📂 Copying deploy files to remote server..."
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'
                    rsync -avz docker-compose.deploy.yml nginx.conf \
                        ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/
                """
            }
        }

        stage('Deploy (Blue-Green Switch)') {
            steps {
                script {
                    def nextColor = ""
                    def currentColor = ""

                    // 🔍 Find currently active color on remote server
                    currentColor = sh(
                        script: "ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'cat ${ACTIVE_COLOR_FILE} || echo none'",
                        returnStdout: true
                    ).trim()

                    if (currentColor == "blue") {
                        nextColor = "green"
                    } else {
                        nextColor = "blue"
                    }

                    echo "🎨 Current active: ${currentColor}, deploying new: ${nextColor}"

                    // 🚀 Deploy next environment
                    sh """
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                            cd ${DEPLOY_PATH} &&
                            docker compose -f docker-compose.deploy.yml up -d frontend_${nextColor} backend_${nextColor} db_${nextColor}
                        '
                    """

                    // ⏳ Health check (wait 20s and test)
                    sleep 20
                    def health = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' http://${DEPLOY_HOST}/",
                        returnStdout: true
                    ).trim()

                    if (health == "200") {
                        echo "✅ Health check passed! Switching traffic to ${nextColor}"

                        sh """
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                                sed -i "s/frontend_${currentColor}/frontend_${nextColor}/" ${DEPLOY_PATH}/nginx.conf
                                docker restart nginx_proxy
                                echo ${nextColor} > ${ACTIVE_COLOR_FILE}
                            '
                        """
                    } else {
                        echo "❌ Health check failed! Rolling back to ${currentColor}"
                        sh """
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                                docker compose -f ${DEPLOY_PATH}/docker-compose.deploy.yml stop frontend_${nextColor} backend_${nextColor} db_${nextColor}
                            '
                        """
                        error("Deployment failed, rollback done")
                    }
                }
            }
        }
    }
}


