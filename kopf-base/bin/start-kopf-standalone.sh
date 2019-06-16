#!/bin/bash

NAMESPACE=`cat /var/run/secrets/kubernetes.io/serviceaccount/namespace`

if [ ! -f handlers.py ]; then
    echo "ERROR: Missing operator handlers.py file for kopf. Exiting."
    exit 1
fi

if [ x"$PYTHONPATH" != x"" ]; then
    PYTHONPATH=/opt/app-root/src:$PYTHONPATH
else
    PYTHONPATH=/opt/app-root/src
fi

export PYTHONPATH

# --verbose

exec kopf run handlers.py --standalone --namespace=$NAMESPACE
