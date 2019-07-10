OpenShift doesn't provide a way of easily deploying multiple templates at the same time which share parameters.

Thus, rather than have a template for deploying a web front end using an S2I builder image, and another for deploying a database, and processing both at the same time to create a combined deployment, you are forced to do them separately, or create a single template which duplicates parts from each. You don't have a library of templates which could be used as building blocks to create a larger application consisting of multiple components. With this operator you could.

Since there aren't existing templates for triggering S2I builder based applications, well use MongoDB again, but deploy two instances of it. Just pretend one usage of it represents the non existent template for deploying a web application using an S2I builder.

For this we will create a template which you can see by running:

```execute
cat examples/frontend-plus-database.yaml
```

You should see:

```
kind: Template
apiVersion: template.openshift.io/v1
metadata:
  name: frontend-plus-database
parameters:
- name: NAME
  value: myapplication
- name: DATABASE_PASSWORD
  from: '[a-zA-Z0-9]{16}'
  generate: expression
  required: true
objects:
- kind: Dropper
  apiVersion: example.openshift.dev/v1
  metadata:
    name: ${NAME}-frontend
  spec:
    template:
      mongodb-ephemeral
    parameters:
    - name: DATABASE_SERVICE_NAME
      value: ${NAME}-frontend
    - name: MONGODB_PASSWORD
      value: ${DATABASE_PASSWORD}
- kind: Dropper
  apiVersion: example.openshift.dev/v1
  metadata:
    name: ${NAME}-backend
  spec:
    template:
      mongodb-ephemeral
    parameters:
    - name: DATABASE_SERVICE_NAME
      value: ${NAME}-database
    - name: MONGODB_PASSWORD
      value: ${DATABASE_PASSWORD}
```

Create the template.

```execute
oc apply -f examples/frontend-plus-database.yaml
```

This loads it into the project but doesn't process it. The idea here is that this would be something that would pre-exist in your template catalog that you could use.

With this existing, we next need our custom resource for creating our application. You can see it by running:

```execute
cat examples/myapplication.yaml
```

You should see:

```
kind: Dropper
apiVersion: example.openshift.dev/v1
metadata:
  name: myapplication
spec:
  template:
    frontend-plus-database
  parameters:
  - name: NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
  - name: DATABASE_PASSWORD
    valueFrom:
        secretKeyRef:
            name: mongodb-credentials
            key: MONGODB_PASSWORD
```

Create this:

```execute
oc apply -f examples/myapplication.yaml
```

You will see it create `droppers/myapplication`, but as the template it triggers in turn contains further instances of `Dropper`, that triggers those as well. To see them all, run:

```execute
oc get droppers -o name
```

The end result is the MongoDB template will be instantiated twice. The one which we are using to pretend is the frontend, and that for the actual database backend. Run:

```execute
oc get all -o name
```

and you should see deployments and other resources corresponding to both the front end and backend.

To delete everything create from all the templates, we only need delete the top level custom resource.

```execute
oc delete dropper/myapplication
```
