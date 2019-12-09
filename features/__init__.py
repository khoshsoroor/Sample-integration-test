from io import StringIO
from typing import Any

import yaml
import logging
from aloe import before, step, world
from datetime import datetime

from catalyst import service_invoker
from catalyst.service_invoker import get_swagger_operations
import requests

REFERENCE_DATE = datetime.strptime('Jan 01 1970  12:00AM', '%b %d %Y %I:%M%p')
REFERENCE_DATE_DATE = REFERENCE_DATE.date()


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k, v in self.__dict__.items():
            if type(v) == dict:
                setattr(self, k, Struct(**v))


f = open('config.yml', 'rt')
config: Any = Struct(**yaml.load(f.read(), Loader=yaml.FullLoader))


logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('test_ostadkar.txt', 'wt', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


swagger = requests.get(config.swagger_url)
service_invoker.operations = get_swagger_operations(StringIO(swagger.text))
service_invoker.base_url = config.service_discovery_url


@step(r'Status code must be (\d+)')
def check_result_add_cities(_, status_code: int):
    assert world.status_code == int(status_code)


@before.each_step
def log(*args):
    logger.debug('Request: ' + str(args))
