#!/bin/bash

set -x
set -eo pipefail

WORKSHOP_NAME=lab-dropper-operator
JUPYTERHUB_APPLICATION=${JUPYTERHUB_APPLICATION:-lab-dropper-operator}
JUPYTERHUB_NAMESPACE=`oc project --short`

oc delete all --selector build="$WORKSHOP_NAME"
