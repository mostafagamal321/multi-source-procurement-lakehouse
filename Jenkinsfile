pipeline {
  agent any

  options {
    timestamps()
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

    stage('Run Tests') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. pytest -q"'
      }
    }

    stage('Run Lint') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && ruff check ."'
      }
    }

    stage('Generate Sources') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/generate_sample_sources.py"'
      }
    }

    stage('Upload Sources to MinIO') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/upload_sources_to_minio.py"'
      }
    }

    stage('Run Lakehouse Pipeline') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/run_local_pipeline.py"'
      }
    }

    stage('Run Quality Checks') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/run_quality_checks.py"'
      }
    }

    stage('Upload Outputs to MinIO') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/upload_outputs_to_minio.py"'
      }
    }

    stage('Load Silver to PostgreSQL') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app && PYTHONPATH=. python scripts/load_silver_to_postgres.py"'
      }
    }

    stage('Run dbt Build and Tests') {
      steps {
        sh 'docker compose run --rm app-worker sh -lc "cd /opt/app/dbt && dbt build --profiles-dir ."'
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

  post {
    always {
      sh '''
        mkdir -p reports
        docker compose logs --no-color > reports/docker-compose.log || true
      '''
      archiveArtifacts artifacts: 'reports/docker-compose.log', allowEmptyArchive: true
    }
  }
}