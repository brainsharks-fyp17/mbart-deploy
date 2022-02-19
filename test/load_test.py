import os
import signal
import time
import random

import gevent
import gevent.monkey
import logging

gevent.monkey.patch_all()
from locust import HttpUser, task, between, constant
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_printer, stats_history
from input import text

setup_logging("INFO", None)
logger = logging.getLogger("pytest")


class Backend:
    def __init__(self):
        import subprocess
        self.process = subprocess.Popen(["python3", "../backend/main.py"])
        time.sleep(25)

    def kill(self):
        os.killpg(os.getpgid(self.process.pid), signal.SIGHUP)


def get_random_text() -> str:
    output = ""
    for i in range(random.randint(2, 15)):
        output += random.choice(text) + " "
    return output + "."


class BackendUser(HttpUser):
    # wait_time = constant(1)
    host = "http://localhost:8000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def on_start(self):
    #     logger.info("Starting the backend")
    #     self.backend = Backend()

    # def on_stop(self):
    #     logger.info("Killing the backend")
    #     self.backend.kill()
    #     time.sleep(5)

    @task
    def generate_task(self):
        data = {"text": get_random_text()}
        self.client.post("/generate", data=data)


def test_load(users=1, spawn_rate=2, time_s=60):
    # setup Environment and Runner
    backend = Backend()
    env = Environment(user_classes=[BackendUser])
    env.create_local_runner()

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test
    env.runner.start(users, spawn_rate=spawn_rate)

    # in 60 seconds stop the runner
    gevent.spawn_later(time_s, lambda: env.runner.quit())

    # wait for the greenlets
    env.runner.greenlet.join()

    logger.info("Average Response Time: " + str(env.stats.total.avg_response_time))
    logger.info("Number of Failures: " + str(env.stats.total.num_failures))
    logger.info("Response time percentile<(0.95): " + str(env.stats.total.get_response_time_percentile(0.95)))
    assert env.stats.total.avg_response_time < 60
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 100

    # backend.kill()
    # todo kill the backend


if __name__ == '__main__':
    # test_load(users=1, spawn_rate=5, time_s=15)
    print(get_random_text())