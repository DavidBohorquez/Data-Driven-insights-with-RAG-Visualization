pipeline {
    agent any

    environment {
        SERVICE = 'sqlite'
    }

    stages {
        stage('Install dependencies') {
            steps {
                echo "Installing Python dependencies for ${SERVICE} service..."
                sh. "docker-compose exec $SERVICE pip install -r requirements.txt"
            }
        }

        stage('Run tests') {
            steps {
                echo "Running pytest for ${SERVICE} service..."
                sh "docker-compose exec $SERVICE pytest /app/tests --maxfail=1 --disable-warnings --tb=short -v"
            }
        }

        stage('Build Docker image') {
            steps {
                echo "Rebuilding Docker images..."
                sh 'docker-compose build'
            }
        }

        stage('Notify') {
            steps {
                mail to: 'ndbohorquezg@gmail.com',
                        subject: "CI Pipeline Passed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: "All stages passed for ${env.JOB_NAME} #${env.BUILD_NUMBER}. " +
                              "Check console output at ${env.BUILD_URL} to view the results."
            }
        }
    }

    post {
        failure {
            mail to: 'ndbohorquezg@gmail.com',
                    subject: "CI Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: "One or more stages failed for ${env.JOB_NAME} #${env.BUILD_NUMBER}. " +
                          "Check console output at ${env.BUILD_URL} to view the results."
        }
    }
}