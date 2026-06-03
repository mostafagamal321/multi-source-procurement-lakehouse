pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout(true)
  }

  environment {
    COMPOSE_PROJECT_NAME = 'multi-source-procurement-lakehouse'
    OFFLINE_API_MODE = 'true'
  }

  stages {
    stage('Checkout') {
      steps {
        retry(3) {
          sh '''
            set -eux
            find . -mindepth 1 -maxdepth 1 -exec rm -rf {} +
            git init .
            git remote add origin https://github.com/mostafagamal321/multi-source-procurement-lakehouse.git
            git fetch --depth=1 --no-tags origin main
            git checkout -f FETCH_HEAD
          '''
        }
      }
    }

    stage('Show Environment') {
      steps {
        sh '''
          pwd
          git --version
          docker --version
          docker compose version
        '''
      }
    }