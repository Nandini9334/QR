
pipeline {
    agent any

    stages {
        stage('Validate Flask files') {
            steps {
                bat '"C:\\Users\\POTTA NANDINI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'

                bat '"C:\\Users\\POTTA NANDINI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'

                bat '"C:\\Users\\POTTA NANDINI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m py_compile app.py'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t nandini9334/qr-code-generator:%BUILD_NUMBER% -t nandini9334/qr-code-generator:latest .'
            }
        }

        stage('Push image to Docker Hub') {
            steps {
                bat 'docker login -u nandini9334 -p dhinnu@18'

                bat 'docker push nandini9334/qr-code-generator:%BUILD_NUMBER%'

                bat 'docker push nandini9334/qr-code-generator:latest'
            }
        }


    
}
post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
