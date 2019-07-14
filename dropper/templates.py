import yaml
import json
import rstr

from api import client, namespace, ApiException

class Template(object):

    def __init__(self, data):
        self._data = data
        self._validate()

    def _validate(self):
        if not isinstance(self._data, dict):
            raise ValueError("template data is not a dict")

        if "apiVersion" not in self._data:
            raise ValueError("template data doesn't specify api")
        if self._data["apiVersion"] not in ("v1", "template.openshift.io/v1"):
            raise ValueError("template data type not a template")

        if "kind" not in self._data:
            raise ValueError("template data doesn't specify type")
        if self._data["kind"] != "Template":
            raise ValueError("template data type not a template")

        if "metadata" not in self._data:
            raise ValueError("template data doesn't specify metadata")

        if "name" not in self._data["metadata"] or not self._data["metadata"]["name"]:
            raise ValueError("template doesn't specify name")

        if "parameters" not in self._data:
            raise ValueError("template doesn't specify parameters")
        if not isinstance(self._data["parameters"], list):
            raise ValueError("template parameters not a list")

        if "objects" not in self._data:
            raise ValueError("template doesn't specify objects")
        if not isinstance(self._data["parameters"], list):
            raise ValueError("template objects not a list")

    @property
    def name(self):
        return self._data["metadata"]["name"]

    @property
    def parameters(self):
        return self._data["parameters"]

    @property
    def objects(self):
        return self._data["objects"]

    def _generate_value(self, pattern):
        return rstr.xeger(pattern)

    def _evaluate_parameter(self, param, value=None):
        if value is None:
            if "value" in param:
                return param["value"]
            elif "generate" in param and param["generate"] == "expression":
                value = self._generate_value(param["from"])
                return value
            else:
                return ""
        else:
            return value

    def _expand_parameters(self, inputs={}):
        parameters = {}
        for param in self.parameters:
            name = param["name"]
            value = self._evaluate_parameter(param, inputs.get(name))
            if not value and param.get("required", False):
                raise ValueError("parameter %s is required and must be specified" % param["name"])
            parameters[name] = value
        return parameters

    def _substitute_value(self, value, parameters):
        if value.startswith("${{") and value.endswith("}}"):
            token = value[3:-2]
            for key, val in parameters.items():
                if key == token:
                    try:
                        value = json.loads(val) 
                    except JSONDecodeError:
                        pass
                    break
        else:
            for key, val in parameters.items():
                value = value.replace("${%s}" % key, val)
        return value

    def _process_object(self, obj, parameters):
        if isinstance(obj, list):
            return [self._process_object(val, parameters) for val in obj] 
        elif isinstance(obj, dict):
            return {self._process_object(key, parameters):self._process_object(val,
                    parameters) for key,val in obj.items()}
        elif isinstance(obj, str):
            return self._substitute_value(obj, parameters)
        else:
            return obj

    def _interpolate_objects(self, parameters):
        for obj in self.objects:
            yield self._process_object(obj, parameters)

    def expand(self, inputs={}):
        parameters = self._expand_parameters(inputs)
        return list(self._interpolate_objects(parameters))

def loads_json(data):
    return Template(json.loads(data))

def loads_yaml(data):
    return Template(yaml.safe_load(data))

def load_json(filename):
    with open(filename) as fp:
        return loads_json(fp.read())

def load_yaml(filename):
    with open(filename) as fp:
        return loads_yaml(fp.read())

template_resource = client.resources.get(api_version="template.openshift.io/v1",
        kind="Template", singular_name='template')

def process_template(name, params, logger):
    try:
        project, name = name.split('/', 1)
    except ValueError:
        project = namespace

    try:
        resource = template_resource.get(namespace=project, name=name)

    except ApiException as e:
        if e.status != 404:
            logger.exception('Error loading template %s from %s.', (name, project))
            raise

    except Exception as e:
        logger.exception('Error loading template %s from %s.', (name, project))
        raise

    template = Template(resource.to_dict())

    return template.expand(params)
