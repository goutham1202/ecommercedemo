pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
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
                    pytest
                '''
            }
        }

        stage('Run Performance Tests') {
            steps {
                echo 'Running system performance test...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    python performance_test.py
                '''

                echo 'Running load test...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    locust -f load_test.py --headless -u 5 -r 1 --run-time 1m
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
            echo 'Pipeline failed!'
        }
    }
}
