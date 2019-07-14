import kopf

from parameters import parse_parameters
from templates import process_template
from resources import create_resources

@kopf.on.create('example.openshift.dev', 'v1', 'templatebindings')
def create(name, namespace, uid, spec, logger, **_):
    logger.info('CREATE: %s %s', name, spec)
    params = parse_parameters(name, namespace, spec.get("parameters", []))
    resources = process_template(spec["template"], params, logger)
    items = create_resources(resources, uid, logger)
    return { 'resources-created': len(items) }
