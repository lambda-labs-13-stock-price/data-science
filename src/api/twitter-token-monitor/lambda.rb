require 'aws-sdk-sqs'
require 'json'

REGION = ENV['AWS_REGION_CODE']
QUEUE_URL = ENV['AWS_SQS_URL']

def handle(event:, context:)
  sqs = Aws::SQS::Client.new(region: REGION)
  message = 'success'
  status = 200
  headers = {
    "Content-Type" => "application/json"
  }

  if event["httpMethod"] == "POST"
    sqs.send_message(queue_url: QUEUE_URL, message_body: event.to_json )
  else
    status = 400
    message = 'invalid request'
  end

  {
    'statusCode' => status,
    'headers' => headers,
    'body' => { "message" => message }.to_json
  }
end
