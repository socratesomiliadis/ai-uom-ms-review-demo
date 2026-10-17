// Teaching equivalent: use a disposable Linux worker with JDK 17, Python 3 and Git.
// In production the trusted job definition must live outside the candidate PR.
pipeline {
    agent { label 'java17-disposable' }
    parameters {
        string(name: 'TRUSTED_BASE_SHA', defaultValue: '', description: 'Reviewed base commit SHA supplied by the instructor or PR integration')
    }
    options { timeout(time: 10, unit: 'MINUTES'); skipDefaultCheckout(true) }
    stages {
        stage('Checkout candidate') { steps { dir('candidate') { checkout scm } } }
        stage('Checkout trusted policy') {
            steps {
                script {
                    if (!(params.TRUSTED_BASE_SHA ==~ /[0-9a-fA-F]{40}/)) {
                        error('Set TRUSTED_BASE_SHA to a reviewed 40-character SHA')
                    }
                }
                sh '''
                    git clone --no-hardlinks candidate policy
                    git -C policy checkout --detach "$TRUSTED_BASE_SHA"
                '''
            }
        }
        stage('Evaluate candidate') {
            steps { sh 'python3 policy/ci/evaluate.py --candidate candidate --trusted policy --mode acceptance --out reports' }
        }
    }
    post {
        always {
            junit testResults: 'reports/junit/TEST-*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/result.json,reports/build.log,reports/junit/*.xml', allowEmptyArchive: true
        }
    }
}
