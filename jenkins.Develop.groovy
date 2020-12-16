def build_app(){
  sh 'docker compose up -d'
}

def test_app(){
  sh 'locust -f test.py -u 1000 -r 20 -H http://0.0.0.0:8050/ -t 1m --headless'
}

def down_app(){
  sh 'docker compose down'
}

def release_app(){
  echo 'Ready to be merge to release'
}


return this
