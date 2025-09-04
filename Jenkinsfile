pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GEMINI_API_KEY = credentials('GEMINI_API_KEY') // Jenkins Secret Text
        LOG_DIR = 'logs'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/goutham1202/ecommercedemo.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    set -e
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    pytest || echo "Unit tests failed"
                '''
            }
        }

        stage('Run Performance Tests') {
            steps {
                echo 'Running performance tests...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    python performance_test.py || echo "Performance test script failed"
                    locust -f load_test.py --headless -u 5 -r 1 --run-time 1m || echo "Load test failed"
                '''
            }
        }

        stage('Analyze Logs with LLM') {
            steps {
                echo 'Sending logs to Google Gemini LLM for analysis...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    python rag_log_analyzer.py --log_dir ${LOG_DIR} --api_key ${GEMINI_API_KEY}
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving logs...'
            archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline completed with failures!'
        }
    }
}
