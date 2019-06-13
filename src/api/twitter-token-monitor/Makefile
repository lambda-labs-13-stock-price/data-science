NAME := twitter-token-monitor
ZIPFILE := $(NAME).zip

CONFIG := cloudformation.yaml

AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --output text --query 'Account')

AWS_LAMBDA_NAME ?= $(NAME)
AWS_LAMBDA_HANDLER ?= lambda.handle
AWS_LAMBDA_RUNTIME ?= ruby2.5
AWS_LAMBDA_ROLE_NAME ?= aws-lambda-$(NAME)
AWS_LAMBDA_ROLE_ARN ?= arn:aws:iam::$(AWS_ACCOUNT_ID):role/$(AWS_LAMBDA_ROLE_NAME)

clean:
	rm $(ZIPFILE)
	rm -rf vendor

validate: $(CONFIG) 
	aws cloudformation validate-template --template-body file://$(CONFIG)

vendor: Gemfile
	bundle install --gemfile=Gemfile --path vendor/bundle

$(ZIPFILE): lambda.rb vendor
	zip $@ lambda.rb
	zip -r $@ vendor

create: $(ZIPFILE) 
	aws lambda create-function \
		--function-name $(AWS_LAMBDA_NAME) \
		--handler $(AWS_LAMBDA_HANDLER) \
		--runtime $(AWS_LAMBDA_RUNTIME) \
		--role $(AWS_LAMBDA_ROLE_ARN) \
		--zip-file fileb://$(ZIPFILE)

update: clean hidden-alphabet-api.zip
	aws lambda update-function-code \
		--function-name $(AWS_LAMBDA_NAME) \ 
		--zip-file fileb://$(ZIPFILE)


