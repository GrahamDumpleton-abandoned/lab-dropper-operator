Parameters can also be filled from separate config maps or secrets.

Create a config map by running:

```execute
oc create configmap database-settings --from-literal DATABASE_MEMORY=1Gi
```

and a secret:

```execute
oc create secret generic database-credentials --from-literal DATABASE_USERNAME=grumpy --from-literal DATABASE_PASSWORD=password
```

To see the custom resource we are going to use this time, run:

```execute
cat examples/database-gamma.yaml
```

You should see:

```
kind: TemplateBinding
apiVersion: example.openshift.dev/v1
metadata:
  name: database-gamma
spec:
  template:
    database
  parameters:
  - name: APPLICATION_NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
  - name: DATABASE_MEMORY
    valueFrom:
        configMapKeyRef:
            name: database-settings
            key: DATABASE_MEMORY
  - name: DATABASE_USERNAME
    valueFrom:
        secretKeyRef:
            name: database-credentials
            key: DATABASE_USERNAME
  - name: DATABASE_PASSWORD
    valueFrom:
        secretKeyRef:
            name: database-credentials
            key: DATABASE_PASSWORD
```

Create the resource:

```execute
oc apply -f examples/database-gamma.yaml
```

To verify that our value was used for the secret, click on the link below:

[%console_url%/k8s/ns/%project_namespace%/secrets/database-gamma-secrets](%console_url%/k8s/ns/%project_namespace%/secrets/database-gamma-secrets)

This should bring up the web console on the secrets for the project. Scroll down and click on "Reveal Values" and you should see "grumpy" for the "DATABASE_USERNAME" field and for "DATABASE_PASSWORD" the value "password".

To verify that our value from the config map was used for memory, click on the link below:

[%console_url%/k8s/ns/%project_namespace%/deploymentconfigs/database-gamma](%console_url%/k8s/ns/%project_namespace%/deploymentconfigs/database-gamma)

This should bring up the deployment config. Scroll down and verify the memory is 1Gi.

Delete it again:

```execute
oc delete templatebinding/database-gamma
```
