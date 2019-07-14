The operator code isn't too complex, and there is still more magic it can do.

The first is that template parameters given in the custom resource don't need to be literal values. The parameters can also be filled in with certain values using a downward API like mechanism as implemented for other builtin resource types, or by referencing values from a config map or secret.

An example of using downward API mechanism can be found by running:

```execute
cat examples/database-beta.yaml
```

You should see:

```
kind: TemplateBinding
apiVersion: example.openshift.dev/v1
metadata:
  name: database-beta
spec:
  template:
    database
  parameters:
  - name: APPLICATION_NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
```

In this case, the `APPLICATION_NAME` parameter is filled out with the value of `metadata.name` from the custom resource. The use of `metadata.namespace` is also supported.

Create the resource by running:

```execute
oc apply -f examples/database-beta.yaml
```

Run:

```execute
oc get dc -o name
```

and you should see that the deployment this time is named `database-beta`.

Delete it when done looking.

```execute
oc delete templatebinding/database-beta
```
