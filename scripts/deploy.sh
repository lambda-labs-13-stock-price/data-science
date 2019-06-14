#!/usr/bin/env bash

aws iam create-policy \
    --policy-name USWest2AdministratorAccessOnly \
    --description "Provides full access in us-west-2 (Oregon) only"\
    --policy-document file://config/us-west-2-deployments-only-policy.json
