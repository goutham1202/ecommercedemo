pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
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
                    mkdir -p ${LOG_DIR}
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    set +e
                    . ${VENV_DIR}/bin/activate
                    pytest > ${LOG_DIR}/unit_tests.log 2>&1
                    test $? -eq 0 || echo "Unit tests failed (see logs/unit_tests.log)"
                '''
            }
        }

        stage('Run Performance Tests') {
            steps {
                echo 'Running performance tests...'
                sh '''
                    set +e
                    . ${VENV_DIR}/bin/activate
                    python performance_test.py > ${LOG_DIR}/performance_test.log 2>&1
                    test $? -eq 0 || echo "Performance tests failed (see logs/performance_test.log)"

                    locust -f load_test.py --headless -u 5 -r 1 --run-time 1m \
                        > ${LOG_DIR}/load_test.log 2>&1
                    test $? -eq 0 || echo "Load test failed (see logs/load_test.log)"
                '''
            }
        }

        stage('Analyze Logs with LLM') {
            steps {
                echo 'Sending logs to Google Gemini LLM for analysis...'
            sh '''
                . ${VENV_DIR}/bin/activate
                echo "===== LLM Analysis Start ====="
                python rag_log_analyzer.py --log_dir ${LOG_DIR} --api_key ${GEMINI_API_KEY}
                echo "===== LLM Analysis End ====="
            '''
            }
        }


    post {
        always {
            echo 'Archiving logs...'
            archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline completed with failures! Check logs for details.'
        }
    }
}
