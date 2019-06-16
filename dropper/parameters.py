import base64

from api import client, namespace, ApiException

configmap_resource = client.resources.get(api_version="v1",
        kind="ConfigMap", singular_name='configmap')
secret_resource = client.resources.get(api_version="v1",
        kind="Secret", singular_name='secret')

def extract_value(crd_name, namespace, param):
    if "valueFrom" in param:
        if "fieldRef" in param["valueFrom"]:
            path = param["valueFrom"]["fieldRef"]["fieldPath"]
            if path == "metadata.name":
                return crd_name
            elif path == "metadata.namespace":
                return namespace
            else:
                raise kopf.HandlerFatalError("Invalid path %s "
                        "for downward API" % fieldPath)

        elif "configMapKeyRef" in param["valueFrom"]:
            name = param["valueFrom"]["configMapKeyRef"]["name"]
            key = param["valueFrom"]["configMapKeyRef"]["key"]

            configmap = configmap_resource.get(namespace=namespace,
                    name=name)

            return configmap["data"][key]

        elif "secretKeyRef" in param["valueFrom"]:
            name = param["valueFrom"]["secretKeyRef"]["name"]
            key = param["valueFrom"]["secretKeyRef"]["key"]

            secret = secret_resource.get(namespace=namespace,
                    name=name)

            return base64.decodestring(
                    secret["data"][key].encode('utf-8')).decode('utf-8')

        else:
            raise kopf.HandlerFatalError("Invalid parameter %s" % param)

    else:
        return param.get("value", "")

def parse_parameters(crd_name, namespace, parameters):
    params = {}

    for param in parameters:
        params[param["name"]] = extract_value(crd_name, namespace, param)

    return params
