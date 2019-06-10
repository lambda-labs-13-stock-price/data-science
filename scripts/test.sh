#!/usr/bin/env bash

STATUS=$(
  aws cloudformation validate-template \
    --template-body file://template.yaml 2>&1
)

if [ $? -ne 0 ]; then
  echo "❌ Validation Failed."
  echo 'Output:'
  echo ${STATUS}
else
  echo "✅ Validation Successful!"
fi


