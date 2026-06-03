
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
    stage('Show Environment') {
      steps {
        sh '''
          pwd
          ls -la
          git --version
          docker --version
          docker compose version
        '''
      }
    }
 
    stage('Validate Docker Compose') {
      steps {
        sh 'docker compose config > /tmp/procurement-compose.yml'
      }
    }
 
    stage('Build Images') {
      steps {
        sh 'docker compose build airflow-webserver airflow-scheduler airflow-init app-worker'
      }
    }
 
    stage('Start Services') {
      steps {
        sh 'docker compose up -d postgres-warehouse minio airflow-init airflow-webserver airflow-scheduler superset'
      }
    }
 
    stage('Run CI Pipeline in App Worker') {
      steps {
        sh '''
          docker rm -f procurement-ci-app-${BUILD_NUMBER} || true
 
          docker run --name procurement-ci-app-${BUILD_NUMBER} \
            --network ${COMPOSE_PROJECT_NAME}_default \
            -e PYTHONPATH=. \
            -e OFFLINE_API_MODE=true \
            -e MINIO_ENDPOINT=minio:9000 \
            -e MINIO_ROOT_USER=minioadmin \
            -e MINIO_ROOT_PASSWORD=minioadmin \
            -e MINIO_SECURE=false \
            -e POSTGRES_HOST=postgres-warehouse \
            -e POSTGRES_PORT=5432 \
            -e POSTGRES_DB=procurement \
            -e POSTGRES_USER=procurement \
            -e POSTGRES_PASSWORD=procurement \
            procurement-app-worker:local \
            sh -lc "
              cd /opt/app &&
              ruff check . &&
              python scripts/generate_sample_sources.py &&
              python scripts/upload_sources_to_minio.py &&
              python scripts/run_local_pipeline.py &&
              python scripts/run_quality_checks.py &&
              python scripts/upload_outputs_to_minio.py &&
              python scripts/load_silver_to_postgres.py &&
              cd dbt &&
              dbt build --profiles-dir .
            "
 
          rm -rf reports dbt/logs
          docker cp procurement-ci-app-${BUILD_NUMBER}:/opt/app/reports ./reports || true
          docker cp procurement-ci-app-${BUILD_NUMBER}:/opt/app/dbt/logs ./dbt/logs || true
          docker rm -f procurement-ci-app-${BUILD_NUMBER} || true
        '''
      }
    }
 
    stage('Show Docker Status') {
      steps {
        sh 'docker compose ps'
      }
    }
 
    stage('Archive Reports') {
      steps {
        archiveArtifacts artifacts: 'reports/data_quality_report.md,reports/data_quality_report.json,reports/pipeline_summary.md,dbt/logs/**/*', allowEmptyArchive: true
      }
    }
  }
}