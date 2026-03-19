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
                bat 'set "DOCKER_BUILDKIT=0" && "%DOCKER_EXE%" build --no-cache -t %IMAGE_NAME% .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '@"%DOCKER_EXE%" rm -f %CONTAINER_NAME% 2>nul || ver > nul'
                bat '"%DOCKER_EXE%" run -d -p 8000:8000 --name %CONTAINER_NAME% -e MONGO_URI=mongodb://host.docker.internal:27017 %IMAGE_NAME%'
                bat '"%POWERSHELL_EXE%" -Command "Start-Sleep -Seconds 10"'
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
                // Debug: confirm Jenkins workspace and test files are visible
                bat 'echo WORKSPACE=%WORKSPACE%'
                bat 'cd'
                bat 'dir'
                bat 'dir tests'
                bat 'type tests\\postman_environment.json | findstr /I /C:"base_url" || echo "postman_environment.json missing or not readable"'
                bat 'findstr /I /C:"pm.test" tests\\postman_collection.json || echo "no pm.test assertions found in collection"'

                // Run Newman
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