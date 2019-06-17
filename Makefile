BASE := .
CONFIG := $(BASE)/config
CLOUDFORMATION := $(CONFIG)/cloudformation
CLOUDFORMATION_CONFIG := $(wildcard $(CLOUDFORMATION)/*.yaml) 

POLICIES := $(CONFIG)/policies
IAM_POLICIES := $(wildcard $(CONFIG)/*.json)
AWS_DEPLOYMENT_REGION_POLICY := $(POLICIES)/us-west-2-deployments-only-policy.json

SUCCEEDING_TEST_CASE="ContextKeyName='aws:RequestedRegion',ContextKeyValues='us-west-2',ContextKeyType=string"
FAILING_TEST_CASE="ContextKeyName='aws:RequestedRegion',ContextKeyValues='eu-west-3',ContextKeyType=string"

define simulate_policy
	aws iam simulate-custom-policy \
		--policy-input-list '$(shell cat $(1) | sed -e 's/^ *//' | tr -d '\n')' \
		--action-names ec2:RunInstances \
		--context-entries $(2)
endef

lint:
	yaml-lint $(CLOUDFORMATION_CONFIG)
	npm run lint

test:
	$(foreach template, $(CLOUDFORMATION_CONFIG), aws cloudformation validate-template --template-body file://$(template);) 
	@echo "Should succeed."
	$(call simulate_policy, $(AWS_DEPLOYMENT_REGION_POLICY), $(SUCCEEDING_TEST_CASE))
	@echo "Should fail."
	$(call simulate_policy, $(AWS_DEPLOYMENT_REGION_POLICY), $(FAILING_TEST_CASE))

deploy:
	aws iam create-policy \
		--policy-name USWest2AdministratorAccessOnly \
		--description "Provides full access in us-west-2 (Oregon) only"\
		--policy-document file://$(AWS_DEPLOYMENT_REGION_POLICY)

clean:
	rm -rf node_modules
	rm package-lock.json
