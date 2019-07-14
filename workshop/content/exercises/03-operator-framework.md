The operator is built using the operator framework `kopf`. To see the main code file for the operator, which defines the handlers which are invoked by the framework, run:

```execute
cat dropper/handlers.py
```

You should see:

```
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
```

In this operator we only care about the notification for when a custom resource is created. The complete code skeleton to handle that is:

```
import kopf

@kopf.on.create('example.openshift.dev', 'v1', 'templatebindings')
def create(name, namespace, uid, spec, logger, **_):
    return {}
```

So we only need to provide a function to handle the callback when the custom resource is created. The decorator applied to the function tells `kopf` what custom resource we want to monitor. We can select what parts of the custom resource we want passed into the function by adding function arguments of the appropriate name. The result from the function is what we want to be added back to the status field of the custom resource.

The body of the function calls out to our custom code for the operator to do the work.

Run:

```execute
ls -las dropper
```

to see all the code files. Use `vi` or `nano` to look at the code they contain.
