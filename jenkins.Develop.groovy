def build_app(){
  sh 'docker-compose up'
}

def test_app(){
  sh 'python test_stress_app.py'
}

def down_app(){
  sh 'docker compose down'
}

def release_app(){
  echo 'Ready to be merge to release'
}

def live_app(){
}

return this
