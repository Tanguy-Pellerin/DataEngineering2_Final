def groovyfile
pipeline {
  agent any
  
  stages {
    stage('Build script') {
      steps {
        script {
          def filename = 'Jenkins.' + env.BRANCH_NAME + '.groovy'
				  groovyfile = load filename
        }
      }
    }
    
    stage('Build web site') {
      steps {
        script {
          groovyfile.build_app()
        }
      }
    }
    
    stage('Testing') {
      steps {
        script {
          groovyfile.test_app()
        }
      }
    }
    
    stage('Down website') {
      steps {
        script {
          groovyfile.down_app()
        }
      }
    }
    
    stage('Merging to release') {
      script {
        groovyfile.release_app()
    }
  }
}
