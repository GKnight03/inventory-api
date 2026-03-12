pipeline {
    agent any

    environment {
        IMAGE_NAME = 'inventory-api'
        CONTAINER_NAME = 'inventory-container'
        PYTHON_EXE = 'C:\\Program Files\\Python312\\python.exe'
        DOCKER_EXE = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe'
        NODE_EXE = 'C:\\Program Files\\nodejs\\node.exe'
        NEWMAN_EXE = 'C:\\Users\\fires\\AppData\\Roaming\\npm\\node_modules\\newman\\bin\\newman.js'
        POWERSHELL_EXE = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
        MONGO_URI = 'mongodb://host.docker.internal:27017'
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
                bat 'set DOCKER_BUILDKIT=0 && "%DOCKER_EXE%" build --no-cache -t %IMAGE_NAME% .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '@"%DOCKER_EXE%" rm -f %CONTAINER_NAME% 2>nul || ver > nul'
                bat '"%DOCKER_EXE%" run -d -p 8000:8000 --name %CONTAINER_NAME% -e MONGO_URI=%MONGO_URI% %IMAGE_NAME%'
                bat 'timeout /t 10 >nul'
                bat '"%DOCKER_EXE%" ps -a'
                bat '"%DOCKER_EXE%" logs %CONTAINER_NAME%'
            }
        }

        stage('Run Pytest Tests') {
            steps {
                bat '"%PYTHON_EXE%" -m pytest tests/unit_test_api.py'
            }
        }

        stage('Run Newman Tests') {
            steps {
                bat '"%NODE_EXE%" "%NEWMAN_EXE%" run tests/postman_collection.json -e tests/postman_environment.json'
            }
        }

        stage('Create Zip File') {
            steps {
                bat '"%POWERSHELL_EXE%" -Command "$date = Get-Date -Format yyyy-MM-dd-HH-mm-ss; Compress-Archive -Path app,tests,data,Dockerfile,requirements.txt,Jenkinsfile,generate_readme.py,README.txt -DestinationPath complete-$date.zip"'
            }
        }
    }

    post {
        always {
            bat '@"%DOCKER_EXE%" stop %CONTAINER_NAME% 2>nul || ver > nul'
            bat '@"%DOCKER_EXE%" rm %CONTAINER_NAME% 2>nul || ver > nul'
        }
    }
}