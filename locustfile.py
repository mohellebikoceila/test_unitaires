from locust import HttpUser, task, between
from locust import wait_time
import json

class PerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def registerPerf(self):
        self.client.get(url="/")
        self.client.get(url="/book/<competition>/<club>")
        self.client.get(url="/logout")
        # self.client.post(url="/register", data=json.dumps(payload))
        self.client.post("/showSummary", data={'email':'admin'})
        self.client.post("/purchasePlaces", data={'club':'Simply Lift','competition':'Spring Festival','place':'2'})