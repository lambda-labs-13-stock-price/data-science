BASE := .
CONFIG := $(BASE)/config
CLOUDFORMATION := $(CONFIG)/cloudformation
CLOUDFORMATION_CONFIG := $(wildcard $(CLOUDFORMATION)/*.yaml) 

lint:
	yaml-lint $(CLOUDFORMATION_CONFIG)

test:
	$(foreach template, $(CLOUDFORMATION_CONFIG), aws cloudformation validate-template --template-body file://$(template);) 
