pipeline {
    agent any

    environment {
        IMAGE_NAME = 'inventory-api'
        CONTAINER_NAME = 'inventory-container'
        ZIP_NAME = "complete-%BUILD_ID%.zip"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/GKnight03/inventory-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Generate README') {
            steps {
                bat 'python generate_readme.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 8000:8000 --name %CONTAINER_NAME% %IMAGE_NAME%'
            }
        }

        stage('Run Python Unit Tests') {
            steps {
                bat 'pytest tests/unit_test_api.py'
            }
        }

        stage('Run Newman Tests') {
            steps {
                bat 'newman run tests/postman_collection.json -e tests/postman_environment.json'
            }
        }

        stage('Create Final Zip') {
            steps {
                bat '''
                powershell -Command "$date = Get-Date -Format yyyy-MM-dd-HH-mm-ss; Compress-Archive -Path app,tests,data,Dockerfile,requirements.txt,Jenkinsfile,generate_readme.py,README.txt -DestinationPath complete-$date.zip"
                '''
            }
        }
    }

    post {
        always {
            bat 'docker stop %CONTAINER_NAME% || exit 0'
            bat 'docker rm %CONTAINER_NAME% || exit 0'
        }
    }
}
