OpenShift doesn't provide a way of easily deploying multiple templates at the same time which share parameters. You are forced to do them separately, or create a single template which duplicates parts from each. You don't have a library of templates which could be used as building blocks to create a larger application consisting of multiple components. With this operator you could.

For this example we will use the `frontend-plus-database` template which you loaded earlier:

```execute
cat templates/frontend-plus-database.yaml
```

You should see:

```
kind: Template
apiVersion: template.openshift.io/v1
metadata:
  name: frontend-plus-database
parameters:
- name: APPLICATION_NAME
  value: application
- name: DATABASE_USERNAME
  from: "user[a-f0-9]{8}"
  generate: expression
- name: DATABASE_PASSWORD
  from: '[a-zA-Z0-9]{16}'
  generate: expression
objects:
- kind: TemplateBinding
  apiVersion: example.openshift.dev/v1
  metadata:
    name: ${APPLICATION_NAME}-frontend
  spec:
    template:
      frontend
    parameters:
    - name: APPLICATION_NAME
      value: ${APPLICATION}
    - name: DATABASE_URL
      value: postgres://${DATABASE_USERNAME}:${DATABASE_PASSWORD}@${APPLICATION_NAME}-database:5432/blog
    - name: DATABASE_USERNAME
      value: ${DATABASE_USERNAME}
    - name: DATABASE_PASSWORD
      value: ${DATABASE_PASSWORD}
- kind: TemplateBinding
  apiVersion: example.openshift.dev/v1
  metadata:
    name: ${APPLICATION_NAME}-database
  spec:
    template:
      database
    parameters:
    - name: APPLICATION_NAME
      value: ${APPLICATION}-database
    - name: DATABASE_USERNAME
      value: ${DATABASE_USERNAME}
    - name: DATABASE_PASSWORD
      value: ${DATABASE_PASSWORD}
```

As you can see, the `Template` is creating multiple instances of the `TemplateBinding` resource. When instantiated that will in turn trigger the instantiation of the further two templates.

Next we need the custom resource for creating our application using this template. You can see it by running:

```execute
cat examples/application.yaml
```

You should see:

```
kind: TemplateBinding
apiVersion: example.openshift.dev/v1
metadata:
  name: application
spec:
  template:
    frontend-plus-database
  parameters:
  - name: APPLICATION_NAME
    valueFrom:
        fieldRef:
            fieldPath: metadata.name
```

Create this:

```execute
oc apply -f examples/application.yaml
```

You will see it create `templatebinding/application`, but as the template in turn contains the `TemplateBinding` resources, that triggers those as well. To see them all, run:

```execute
oc get templatebindings -o name
```

The end result is the frontend and database template will be instantiated. Run:

```execute
oc get all -o name
```

and you should see deployments and other resources corresponding to both the frontend, called `application`, and the database called `application-database`.

To delete everything create from all the templates, we only need delete the top level custom resource.

```execute
oc delete templatebinding/application
```
