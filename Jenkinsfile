pipeline {
  agent any
  stages {
    stage('initialise something') {
      parallel {
        stage('initialise something') {
          steps {
            echo 'starting jenkins pipeline'
          }
        }
        stage('run a thing') {
          steps {
            sh '''echo "Downloading great wallpaper"
wget "https://i.imgur.com/ae4xtKY.jpg"'''
          }
        }
        stage('sleep test') {
          steps {
            sleep 30
            sh '''pwd
ls'''
          }
        }
      }
    }
    stage('do something?!?!') {
      parallel {
        stage('do something?!?!') {
          steps {
            sleep 10
            echo 'DONE SLEEPING'
          }
        }
        stage('print something') {
          steps {
            echo 'starting stage(?) 2'
          }
        }
      }
    }
  }
}