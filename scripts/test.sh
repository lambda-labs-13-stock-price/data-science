#!/usr/bin/env bash

POLICY=$(cat policy.json | sed -e 's/^ *//' | tr -d '\n')

# Should succeed
aws iam simulate-custom-policy \
    --policy-input-list $POLICY \
    --action-names ec2:RunInstances \
    --context-entries "\
        ContextKeyName='aws:RequestedRegion',\
        ContextKeyValues='us-west-2',\
        ContextKeyType=string\
    "

# Should fail
aws iam simulate-custom-policy \
    --policy-input-list $POLICY \
    --action-names ec2:RunInstances \
    --context-entries "\
        ContextKeyName='aws:RequestedRegion',\
        ContextKeyValues='eu-west-3',\
        ContextKeyType=string\
    "