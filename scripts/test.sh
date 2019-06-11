#!/usr/bin/env bash

POLICY=$(cat policy.json | sed -e 's/^ *//' | tr -d '\n')

SUCCESSFUL_CONTEXT="\
ContextKeyName='aws:RequestedRegion',\
ContextKeyValues='us-west-2',\
ContextKeyType=string\
"

FAILING_CONTEXT="\
ContextKeyName='aws:RequestedRegion',\
ContextKeyValues='eu-west-3',\
ContextKeyType=string\
"

# Should succeed
aws iam simulate-custom-policy \
    --policy-input-list "${POLICY}" \
    --action-names ec2:RunInstances \
    --context-entries $SUCCESSFUL_CONTEXT

# Should fail
aws iam simulate-custom-policy \
    --policy-input-list "${POLICY}" \
    --action-names ec2:RunInstances \
    --context-entries $FAILING_CONTEXT
