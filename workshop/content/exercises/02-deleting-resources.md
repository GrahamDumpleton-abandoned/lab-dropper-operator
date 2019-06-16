---
Title: Deleting Resources
PrevPage: 01-template-processing
NextPage: 03-operator-framework
---

The operator can can be used to create any resources specified by a template, but it does more than just that.

One thing it does is to set up owner references for any resources created from the template. This is useful in the case of the MongoDB database template used because it doesn't label all the resources it creates in the same way. It is therefore not possible to delete all resources for the MongoDB database by using a label selector.

Because the operator made all the resources created children of the custom resource, we can run:

```execute
oc delete templatebinding/mongodb-alpha
```

and not only will it delete the custom resource, it will delete all resources associated with the MongoDB database.

If you run:

```execute
oc get all -o name
```

now, you should see that the resources have been deleted, or are in the process of being deleted. Keep running the command until all those for the MongoDB database are gone.
