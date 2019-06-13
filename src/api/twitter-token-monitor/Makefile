NAME := twitter-token-monitor
ZIPFILE := $(NAME).zip

CONFIG := cloudformation.yaml

AWS_ARN := arn:aws:iam::465245944185:role/aws-lambda-$(NAME)

validate: $(CONFIG) 
	aws cloudformation validate-template --template-body file://$(CONFIG)

vendor: Gemfile
	bundle install --gemfile=Gemfile --path vendor/bundle

$(ZIPFILE): lambda.rb vendor
	zip $@ lambda.rb
	zip -r $@ vendor

create: $(ZIPFILE) 
	aws lambda create-function \
		--function-name $(NAME) \
		--handler lambda.handle \
		--runtime ruby2.5 \
		--role $(AWS_ARN) \
		--zip-file fileb://$(ZIPFILE)

update: hidden-alphabet-api.zip
	aws lambda update-function-code \
		--function-name $(NAME) \ 
		--zip-file fileb://$(ZIPFILE)

clean:
	rm $(ZIPFILE)
	rm -rf vendor
