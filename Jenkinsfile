pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([
              $class: 'GitSCM',
              branches: [[name: env.GIT_BUILD_REF]],
              userRemoteConfigs: [[
                url: env.GIT_REPO_URL,
                credentialsId: env.CREDENTIALS_ID
            ]]
        ])
      }
    }
    stage('构建') {
      script {
        docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
          docker.build("${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF}", "--pull .")
        }
      }
    }
    stage('推送制品') {
      script {
        docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
          def image=docker.image("${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF}")
          image.push()
          image.push("latest")
        }
      }
    }
  }
  environment {
    IMAGE_NAME = 'eform/auth-broker'
    DOCKER_TAG = 'broker'

    ENTERPRISE = 'eform-amber'
    PROJECT = 'eform-auth'
    ARTIFACT_REPO = 'docker'
    
    ARTIFACT_BASE = '${ENTERPRISE}-docker.pkg.coding.net'
    ARTIFACT_IMAGE = '${ARTIFACT_BASE}/${PROJECT}/${ARTIFACT_REPO}/${DOCKER_TAG}'
  }
}