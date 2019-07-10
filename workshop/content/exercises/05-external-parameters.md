Parameters can also be filled from separate config maps or secrets.

Create a config map by running:

```execute
oc create configmap mongodb-settings --from-literal MEMORY_LIMIT=1Gi
```

and a secret:

```execute
oc create secret generic mongodb-credentials --from-literal MONGODB_PASSWORD=grumpy
```

To see the custom resource we are going to use this time, run:

```execute
cat examples/mongodb-gamma.yaml
```

You should see:

```
kind: Dropper
apiVersion: example.openshift.dev/v1
metadata:
  name: mongodb-gamma
spec:
  template:
    mongodb-ephemeral
  parameters:
  - name: DATABASE_SERVICE_NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
  - name: MEMORY_LIMIT
    valueFrom:
        configMapKeyRef:
            name: mongodb-settings
            key: MEMORY_LIMIT
  - name: MONGODB_PASSWORD
    valueFrom:
        secretKeyRef:
            name: mongodb-credentials
            key: MONGODB_PASSWORD
```

Create the resource:

```execute
oc apply -f examples/mongodb-gamma.yaml
```

To verify that our value was used for the secret, click on the link below:

[%console_url%/k8s/ns/%project_namespace%/secrets/mongodb-gamma](%console_url%/k8s/ns/%project_namespace%/secrets/mongodb-gamma)

This should bring up the web console on the secrets for the project. Scroll down and click on "Reveal Values" and you should see "grumpy" for the "DATABASE-PASSWORD" field.

To verify that our value from the config map was used for memory, click on the link below:

[%console_url%/k8s/ns/%project_namespace%/deploymentconfigs/mongodb-gamma](%console_url%/k8s/ns/%project_namespace%/deploymentconfigs/mongodb-gamma)

This should bring up the deployment config. Scroll down and verify the memory is 1Gi.

Delete it again:

```execute
oc delete dropper/mongodb-gamma
```
