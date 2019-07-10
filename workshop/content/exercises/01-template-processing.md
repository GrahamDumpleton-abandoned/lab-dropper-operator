The purpose of the operator is to process OpenShift templates and to create the resources generated from the template. This is triggered by creating a custom resource, which lists the name of the template and the parameters. The name of the custom resource type is `Dropper`.

Lets start with a quick example using an existing template provided by OpenShift. The definition for our instance of the `Dropper` resource can be seen by running:

```execute
cat examples/mongodb-alpha.yaml
```

You should see:

```
kind: Dropper
apiVersion: example.openshift.dev/v1
metadata:
  name: mongodb-alpha
spec:
  template:
    mongodb-ephemeral
  parameters:
  - name: DATABASE_SERVICE_NAME
    value: mongodb-alpha
```

Now run:

```execute
oc apply -f examples/mongodb-alpha.yaml
```

This creates the resource `dropper/mongodb-alpha`.

It also though triggers the deployment of a MongoDB database using the `mongodb-ephemeral` template.

To see all the resources we currently have in the project run:

```execute
oc get all -o name
```

You can monitor the progress of the MongoDB database deployment by running:

```execute
oc rollout status dc/mongodb-alpha
```

Note how the deployment name has been dictated by the value supplied for `DATABASE_SERVICE_NAME` in the custom resource we created.
