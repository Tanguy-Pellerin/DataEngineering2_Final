import logging
from locust import HttpUser, task, between, events


class WebsiteTestUser(HttpUser):
	
    @task(1)
    def hello_world(self):
        self.client.get("/")
	

@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.total_rps < 17:
        logging.error("Test failed due to less than 1000 requests per minute")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0