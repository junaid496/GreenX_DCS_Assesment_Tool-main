pipeline { 
    agent any 

    environment {  
        DB_URL = "mysql+pymysql://root:dbpasswd@db:3306/all_tables"  
        DEPLOY_USER = 'root'  
        DEPLOY_HOST = '192.168.18.116'  
        DEPLOY_PATH = '/root/project'  
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

        stage('Clean Local Repo') {  
            steps {  
                sh '''  
                    echo "Cleaning unnecessary files..."  
                    rm -rf GreenX_DCS_Assesment_Tool_Backend/venv  
                    rm -rf GreenX_DCS_Assesment_Tool_Backend/__pycache__  
                    rm -rf greenX-assessment-tool-frontend/node_modules || true  
                '''  
            }  
        }  

        stage('Copy Project to Deployment Server') {  
            steps {  
                sshagent(['ssh-root-key']) {  
                    sh """  
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'mkdir -p ${DEPLOY_PATH}'  
                        scp -o StrictHostKeyChecking=no -r \  
                            GreenX_DCS_Assesment_Tool_Backend \  
                            greenX-assessment-tool-frontend \  
                            docker-compose.yml \  
                            Jenkinsfile \  
                            README.md \  
                            ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/  
                    """  
                }  
            }  
        }  

        stage('Deploy on Remote Server') {  
            steps {  
                sshagent(['ssh-root-key']) {  
                    sh """  
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '  
                            cd ${DEPLOY_PATH} &&  
                            mkdir -p data/db data/backend data/frontend &&  
                            export DB_URL="${DB_URL}" &&  
                            docker compose down || true &&  
                            docker compose up --build -d  
                        '  
                    """  
                }  
            }  
        }  
    }  
}


