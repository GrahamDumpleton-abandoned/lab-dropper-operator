---
Sort: 2
Title: Demo Setup
PrevPage: index
NextPage: exercises/01-template-processing
ExitSign: Start Demo
---

Before we can start, we need to wait for the build of an S2I enabled `kopf` base image to complete. This S2I builder image will be used to build the operator. To monitor the build, run:

```execute
oc logs -f bc/kopf-base
```

Next we need to trigger a build of the image for the operator itself.

```execute
oc start-build dropper-operator --from-dir dropper --follow
```

When this has completed, we wait for it to deploy.

```execute
oc rollout status dc/dropper-operator
```

The operator when running reacts to the creation of a custom resource. The custom resource definition (CRD) has already been loaded. You can see the definition of the CRD by running:

```execute
cat .workshop/resources/customresourcedefinitions.yaml
```

Because the operator is going to need to create resources, it runs with its own service account which has been granted the roles it needs. To See the roles it has been granted, run:

```execute
cat .workshop/resources/clusterroles.yaml
```

With the operator deployed, we are ready to get on with the demo.
