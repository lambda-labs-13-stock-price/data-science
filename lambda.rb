require 'aws-sdk-sqs'
require 'json'

def handle(event:, context:)
  sqs = Aws::SQS::Client.new(region: ENV['AWS_REGION_CODE'])
  message = 'success'
  status = 200
  headers = {
    "Content-Type" => "application/json"
  }

  if event["httpMethod"] == "POST"
    sqs.send_message(queue_url: ENV['AWS_SQS_URL'], message_body: event.to_json )
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
