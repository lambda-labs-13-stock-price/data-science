NAME := hidden-alphabet-api

CONFIG_BASE := config
SRC_BASE := src/functions

SRC := $(SRC_BASE)/lambda.rb

GEMFILE := $(SRC_BASE)/Gemfile
GEMFILE_LOCK := $(GEMFILE).lock

CLOUDFORMATION_CONFIG := $(CONFIG_BASE)/$(NAME)-template.yaml

validate: config/template.yaml
	aws cloudformation validate-template \
		--template-body file://$(CLOUDFORMATION_CONFIG)

vendor: ./Gemfile
	bundle install --gemfile=$(GEMFILE) --path vendor/bundle

$(NAME).zip: $(SRC) vendor
	zip $(NAME).zip $(SRC)
	zip -r $(NAME).zip vendor

create: hidden-alphabet-api.zip
	aws lambda create-function \
		--function-name $(NAME) \
		--handler lambda.handle \
		--runtime ruby2.5 \
		--role arn:aws:iam::465245944185:role/aws-lambda-$(NAME) \
		--zip-file fileb://$(NAME).zip

update: hidden-alphabet-api.zip
	aws lambda update-function-code \
		--function-name $(NAME) \ 
		--zip-file fileb://$(NAME).zip

clean:
	rm $(NAME).zip
	rm -rf vendor
