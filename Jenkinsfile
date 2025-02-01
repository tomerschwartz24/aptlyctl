# Skeleton file for future CI ( probably will move to github CI)
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'pyinstaller aptlyctl.py'
            }
        }
        stage('Test') {
            steps {
                # test aptlyctl commands
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}