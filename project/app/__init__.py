# project/app/__init__.py
import falcon
import json
import logging
import os
from app.tasks import fib
from celery.result import AsyncResult


LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")
logging.basicConfig(level=logging.__getattribute__(LOGLEVEL))

logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")


class Ping(object):
    def on_get(self, req, resp):
        # resp.status = falcon.HTTP_200
        _status_code = 200
        logging.debug("_status_code --> {}".format(_status_code))
        _status = "HTTP_{}".format(_status_code)
        logging.debug("_status --> {}".format(_status))
        resp.status = falcon.__getattribute__(_status)
        logging.debug("resp.status --> {}".format(resp.status))
        resp.body = json.dumps('pong!')


class CreateTask(object):
    def on_post(self, req, resp):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        task = fib.delay(int(result['number']))
        resp.status = falcon.HTTP_200
        result = {
            'status': 'success',
            'data': {
                'task_id': task.id
            }
        }
        resp.body = json.dumps(result)


class CheckStatus(object):
    def on_get(self, req, resp, task_id):
        task_result = AsyncResult(task_id)
        result = {'status': task_result.status, 'result': task_result.result}
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)


app = falcon.API()
app.add_route('/ping', Ping())
app.add_route('/create', CreateTask())
app.add_route('/status/{task_id}', CheckStatus())
