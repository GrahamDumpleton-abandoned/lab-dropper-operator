from api import client, namespace, ApiException

def create_resources(resources, uid, logger):
    if not resources:
        return []

    items = []

    for body in resources:
        try:
            kind = body['kind']
            api_version = body['apiVersion']

            body['metadata']['ownerReferences'] = [dict(
                apiVersion='v1', kind='Namespace', blockOwnerDeletion=False,
                controller=True, name=namespace, uid=uid)]

            resource = client.resources.get(api_version=api_version,
                    kind=kind, singular_name=kind.lower())

            item = resource.create(namespace=namespace, body=body)

            logger.info('RESOURCE: %s/%s/%s', item.kind, item.apiVersion,
                    item.metadata.name)

            items.append(item)

        except ApiException as e:
            if e.status != 409:
                logger.exception('Error creating resource %s.', body)
                raise

            else:
                logger.warn('Resource already exists %s.', body)

        except Exception as e:
            logger.exception('Error creating resource %s.', body)
            raise

    return items
