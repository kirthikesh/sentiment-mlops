pipeline {
    agent any

    environment {
        IMAGE_NAME  = "sentiment-mlops"
        // Set this to your own Docker Hub username/registry in Jenkins
        // (or override via a Jenkins credential/parameter) before first run.
        REGISTRY    = "YOUR_DOCKERHUB_USERNAME"
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        // Jenkins runs as a background service with a minimal PATH, so
        // Homebrew- and Docker Desktop-installed tools (docker, trivy)
        // aren't found by default. Add the common install locations for
        // both Apple Silicon and Intel Macs.
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python3 -m pip install --quiet -r requirements-dev.txt
                    python3 -m flake8 app tests
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 -m pytest tests/test_api.py -v
                '''
            }
        }

        stage('Model Eval Gate') {
            steps {
                // Fails the build if the model's accuracy on the fixed eval
                // set drops below the threshold defined in
                // tests/test_model_eval.py — this is the stage that makes
                // it a real MLOps gate rather than plain CI.
                sh '''
                    . .venv/bin/activate
                    python3 -m pytest tests/test_model_eval.py -v
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Trivy Scan') {
            steps {
                // Fails the build on HIGH/CRITICAL vulnerabilities. exit-code 1
                // makes this a real gate, not just a report.
                sh '''
                    trivy image --severity HIGH,CRITICAL --exit-code 1 --ignorefile .trivyignore --no-progress ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo "Build ${env.BUILD_NUMBER} passed: lint, tests, model-eval gate, scan all green. Image pushed as ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Build ${env.BUILD_NUMBER} failed — check which stage failed above (a failed Model Eval Gate means don't ship this build)."
        }
    }
}
