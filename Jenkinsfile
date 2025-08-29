pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    COMPOSE = 'docker compose'     // agar system me sirf `docker-compose` hai to isko 'docker-compose' kar do
    COMPOSE_PROJECT_NAME = 'greenx'
  }

  triggers {
    githubPush()   // GitHub webhook trigger karega is pipeline ko
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
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

    stage('Build (Compose)') {
      steps {
        sh '''
          ${COMPOSE} build --pull
        '''
      }
    }

    stage('Deploy (Compose)') {
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
      sh '''
        ${COMPOSE} ps
      '''
    }
    failure {
      echo '❌ Build/Deploy failed. Showing recent logs...'
      sh '''
        ${COMPOSE} logs --no-color --since 15m || true
      '''
    }
    always {
      // Logs ko artifact ke taur pe save karna
      sh '''
        ${COMPOSE} logs --no-color --since 15m > compose-latest.log || true
      '''
      archiveArtifacts artifacts: 'compose-latest.log', allowEmptyArchive: true
    }
  }
}

