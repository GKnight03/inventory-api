pipeline {
    agent any

    environment {
        IMAGE_NAME = 'inventory-api'
        CONTAINER_NAME = 'inventory-container'
        PYTHON_EXE = 'C:\\Program Files\\Python312\\python.exe'
    }

    stages {

        stage('Install Python Dependencies') {
            steps {
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }

        stage('Generate README') {
            steps {
                bat '"%PYTHON_EXE%" generate_readme.py'
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

        stage('Run Pytest Tests') {
            steps {
                bat '"%PYTHON_EXE%" -m pytest tests/unit_test_api.py'
            }
        }

        stage('Run Newman Tests') {
            steps {
                bat 'newman run tests/postman_collection.json -e tests/postman_environment.json'
            }
        }

        stage('Create Zip File') {
            steps {
                bat '''
                powershell -Command "$date = Get-Date -Format yyyy-MM-dd-HH-mm-ss; Compress-Archive -Path app,tests,data,Dockerfile,requirements.txt,Jenkinsfile,generate_readme.py,README.txt -DestinationPath complete-$date.zip"
                '''
            }
        }
    }

    post {
        always {
            bat '@docker stop %CONTAINER_NAME% 2>nul || ver > nul'
            bat '@docker rm %CONTAINER_NAME% 2>nul || ver > nul'
        }
    }
}