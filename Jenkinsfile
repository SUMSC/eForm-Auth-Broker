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
        script {
          docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
            docker.build("${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF}", "--pull .")
          }
        }
      }
    }
    stage("推送制品") {
      steps {
        script {
          docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
            def image=docker.image("${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF}")
            image.push()
            image.push("latest")
          }
        }
      }
    }
    stage("部署") {
      steps {
        script {
          def remote = [:]
          remote.name = "qcloud"
          remote.host = "wzhzzmzzy.xyz"
          remote.port = 12450
          remote.user = "amber"
          remote.allowAnyHosts = true
          dockerUser = ""
          dockerPassword = ""
          DOCKER_SERVER = "eform-amber-docker.pkg.coding.net"
          DOCKER_REPO = "${DOCKER_SERVER}/eform-auth/docker"
          BROKER_DOCKER_TAG = "broker"
          BROKER_DOCKER_NAME = "eform-auth-broker"
          BROKER_PORT = "8000"
          LOG_PATH = "/home/amber/eForm-Backend/logs"
          withCredentials([usernamePassword(
            credentialsId: env.CODING_ARTIFACTS_CREDENTIALS_ID,
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASSWORD'
          )]) {
            echo "获取 Docker 认证信息..."
            dockerUser = DOCKER_USER
            dockerPassword = DOCKER_PASSWORD
          }
          withCredentials([sshUserPrivateKey(
            credentialsId: env.QCLOUD_CREDENTIALS_ID,
            keyFileVariable: 'id_rsa'
          )]) {
            echo "开始部署..."
            remote.identityFile = id_rsa
            sshCommand remote: remote, command: "docker login -u ${dockerUser} -p ${dockerPassword} ${DOCKER_SERVER}"
            // eForm-Auth-Broker
            echo "部署 eForm-Auth-Broker"
            sshCommand remote: remote, command: "docker pull ${DOCKER_REPO}/${BROKER_DOCKER_TAG}"
            sshCommand remote: remote, command: "docker stop ${BROKER_DOCKER_NAME} | true"
            sshCommand remote: remote, command: "docker rm ${BROKER_DOCKER_NAME} | true"
            sshCommand remote: remote, command: "docker run --name ${BROKER_DOCKER_NAME} --net host -p 127.0.0.1:${BROKER_PORT}:${BROKER_PORT} -d ${DOCKER_REPO}/${BROKER_DOCKER_TAG}"
          }
        }
      }
    }
  }
  
}