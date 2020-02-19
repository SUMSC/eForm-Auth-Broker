pipeline {
  agent any
  environment {
    IMAGE_NAME = "eform/auth-broker"
    DOCKER_TAG = "broker"

    ENTERPRISE = "eform-amber"
    PROJECT = "eform-auth"
    ARTIFACT_REPO = "docker"
    
    ARTIFACT_BASE = "${ENTERPRISE}-docker.pkg.coding.net"
    ARTIFACT_IMAGE = "${ARTIFACT_BASE}/${PROJECT}/${ARTIFACT_REPO}/${DOCKER_TAG}"
  }
  stages {
    stage("检出") {
      steps {
        checkout([
            $class: "GitSCM",
            branches: [[name: env.GIT_BUILD_REF]],
            userRemoteConfigs: [[
              url: env.GIT_REPO_URL,
              credentialsId: env.CREDENTIALS_ID
          ]]
        ])
      }
    }
    stage("构建") {
      steps {
        echo "${ENTERPRISE}-docker.pkg.coding.net/eform-auth/docker/broker:c159cf5386960b155393666359f3fafa5d789116"
        script {
          docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
            docker.build("${IMAGE_NAME}:${env.GIT_BUILD_REF}", "--pull .")
          }
        }
      }
    }
    stage("推送制品") {
      steps {
        script {
          docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
            def image=docker.image("${IMAGE_NAME}:${env.GIT_BUILD_REF}")
            image.push()
            image.push("latest")
          }
        }
      }
      
    }
  }
  
}