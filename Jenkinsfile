pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/GreenKnight020/inventory-api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t inventory-api .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8000:8000 --name inventory inventory-api'
            }
        }

        stage('Run API Tests') {
            steps {
                bat 'newman run tests/postman_collection.json'
            }
        }

        stage('Generate README') {
            steps {
                bat 'python generate_readme.py'
            }
        }

        stage('Zip Project') {
            steps {
                bat 'powershell Compress-Archive -Path * -DestinationPath complete-%DATE%-%TIME%.zip'
            }
        }

        stage('Stop Container') {
            steps {
                bat 'docker stop inventory'
                bat 'docker rm inventory'
            }
        }

    }
}