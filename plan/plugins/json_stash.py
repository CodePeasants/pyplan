# Python standard library
import os
import json

# 3ps
import appdirs

# Package
import plan
from plan.logger import log
from plan.manager import Manager
from plan.abstract_stash import AbstractStash
from plan.plugin_registry import RegisterMeta


DEFAULT_PATH = appdirs.user_data_dir(appname=plan.__package__, appauthor=plan.__author__, version=plan.__version__)


def get_data_path(**kwargs):
    data_path = kwargs.get('data_path') or DEFAULT_PATH
    return os.path.abspath(os.path.expandvars(data_path))


class JSONStash(AbstractStash, metaclass=RegisterMeta):

    @staticmethod
    def load(**kwargs):
        data_path = get_data_path(**kwargs)

        try:
            with open(data_path, 'r') as fh:
                return Manager.from_dict(json.load(fh))
        except FileNotFoundError:
            log.warning('Data stash file: {data_path} not found.'.format(**locals()))
        return {}

    @staticmethod
    def dump(manager, **kwargs):
        data_path = get_data_path(**kwargs)

        # If the parent directory does not exist, create it.
        data_dir = os.path.dirname(data_path)
        try:
            os.makdirs(data_dir)
        except FileExistsError:
            pass

        with open(data_path, 'w') as fh:
            json.dump(manager.to_dict(), fh)
