from order_reformer_function import app

event = {
  "httpMethod": "POST",
  "body": "{\"appId\":\"KKGFPSVHP85W8\",\"merchants\":{\"VMR1DVW4KS291\":[{\"objectId\":\"O:F2230DCQGTA2A\",\"type\":\"CREATE\",\"ts\":1667030529465}]}}"
}

order = app.lambda_handler(event)
print(order)