# Python standard library
import os
import json

# 3ps
import appdirs

# Package
import plan
from plan.settings import ID_KEY
from plan.object_registry import ObjectRegistry
from plan.exceptions import StashLoadError
from plan.serializable import Serializable
from plan.abstract_stash import AbstractStash
from plan.plugin_registry import RegisterMeta


DEFAULT_PATH = appdirs.user_data_dir(appname=plan.__package__, appauthor=plan.__author__, version=plan.__version__)


def get_data_path(**kwargs):
    data_path = kwargs.get('data_path') or DEFAULT_PATH
    return os.path.abspath(os.path.expandvars(data_path))


class JSONStash(AbstractStash, metaclass=RegisterMeta):
    """
    Basic JSON file storage. This will serialize and load the pyplan data model to/from a single JSON file.
    This will dump and load a Manager object and everything that it recursively references.
    """

    @staticmethod
    def load(**kwargs):
        data_path = get_data_path(**kwargs)

        try:
            with open(data_path, 'r') as fh:
                node_data = json.load(fh)
        except FileNotFoundError:
            raise StashLoadError(f'JSON stash file: {data_path} not found.')

        result = []
        for data in node_data:
            node = Serializable.from_dict(data)
            result.append(node)

        return result

    @staticmethod
    def dump(manager, **kwargs):
        def _recurse(_data, _output=None):
            """
            Recursively get all nodes referenced by the serialized input node.

            :param dict _data:
                Serialized Serializable node.
            :param None|list _output:
                Argument used internally to collect the results of the recursion.
            """
            if _output is None:
                _output = [_data]

            for _key, _value in _data.items():
                if _key != ID_KEY and _value in ObjectRegistry.OBJECTS:
                    _node = ObjectRegistry.get(_value)
                    if _node.id not in [_x.get(ID_KEY) for _x in _output]:
                        _node_data = _node.to_dict()
                        _output.append(_node_data)
                        _recurse(_node_data, _output)
            return _output

        data_path = get_data_path(**kwargs)

        # If the parent directory does not exist, create it.
        data_dir = os.path.dirname(data_path)
        try:
            os.makdirs(data_dir)
        except FileExistsError:
            pass

        # Recursively serialize all of the nodes that the manager references.
        manager_data = manager.to_dict()
        nodes = []
        _recurse(manager_data, nodes)

        with open(data_path, 'w') as fh:
            json.dump(nodes, fh)
