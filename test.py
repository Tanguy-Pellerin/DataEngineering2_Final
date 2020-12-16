from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):
	
    @task(1)
    def hello_world(self):
        self.client.get("/")
"""
    def get_tweet(self):
    	self.client.post("http://0.0.0.0:8050/form_type", json={
    		'sentence': 'The media and establishment want me out of the race so badly -  I WILL NEVER DROP OUT OF THE RACE, WILL NEVER LET MY SUPPORTERS DOWN! #MAGA',
    		})
"""
