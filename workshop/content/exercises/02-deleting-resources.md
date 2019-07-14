The operator can can be used to create any resources specified by a template, but it does more than just that.

One thing it does is to set up owner references for any resources created from the template. This can be useful where a template doesn't label all the resources it creates in a consistent way. When this happens, it may not be possible to delete all resources created by using a single label selector.

Because the operator made all the resources created children of the custom resource, we can run:

```execute
oc delete templatebinding/database-alpha
```

and not only will it delete the custom resource, it will delete all resources associated with the database, regardless of how they were labelled.

If you run:

```execute
oc get all -o name
```

now, you should see that the database resources have been deleted, or are in the process of being deleted. Keep running the command until all those for the database are gone.
