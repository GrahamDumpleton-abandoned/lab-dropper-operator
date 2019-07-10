The operator code isn't too complex, and there is still more magic it can do.

The first is that template parameters given in the custom resource don't need to be literal values. The parameters can also be filled in with certain values using the downward API mechanism used elsewhere in OpenShift, or by referencing values from a config map or secret.

An example of using downward API mechanism can be found by running:

```execute
cat examples/mongodb-beta.yaml
```

You should see:

```
kind: Dropper
apiVersion: example.openshift.dev/v1
metadata:
  name: mongodb-beta
spec:
  template:
    mongodb-ephemeral
  parameters:
  - name: DATABASE_SERVICE_NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
```

In this case, the `DATABASE_SERVICE_NAME` parameter is filled out with the value of `metadata.name` from the custom resource. The use of `metadata.namespace` is also supported.

Create the resource by running:

```execute
oc apply -f examples/mongodb-beta.yaml
```

Run:

```execute
oc get dc -o name
```

and you should see that the deployment this time is named `mongodb-beta`.

Delete it when done looking.

```execute
oc delete dropper/mongodb-beta
```
