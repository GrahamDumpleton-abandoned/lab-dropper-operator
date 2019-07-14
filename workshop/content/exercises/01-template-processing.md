The purpose of the operator is to process OpenShift templates and to create the resources generated from the template. This is triggered by creating a custom resource, which lists the name of the template and the parameters. The name of the custom resource type is `TemplateBinding`.

For the purposes of demonstrating the operator in action, we are going to first load some OpenShift templates into our project.

```execute
oc apply --recursive -f templates/
```

This will result in the following templates being created.

* frontend
* database
* frontend-plus-database

Let's instantiate an instance of the database template. To see a description of the template, including the template parameters it accepts, run:

```execute
oc describe template/database
```

The definition for our instance of the `TemplateBinding` resource, which will be used to trigger the instantiation of the template, can be seen by running:

```execute
cat examples/database-alpha.yaml
```

You should see:

```
kind: TemplateBinding
apiVersion: example.openshift.dev/v1
metadata:
  name: database-alpha
spec:
  template:
    database
  parameters:
  - name: APPLICATION_NAME
    value: database-alpha
```

Now run:

```execute
oc apply -f examples/database-alpha.yaml
```

This creates the resource `templatebinding/database-alpha`.

It also though triggers the deployment of a database using the `database` template.

To see all the resources we now have in the project run:

```execute
oc get all -o name
```

You can monitor the progress of the database deployment by running:

```execute
oc rollout status dc/database-alpha
```

Note how the deployment name has been dictated by the value supplied for `APPLICATION_NAME` in the custom resource we created.
