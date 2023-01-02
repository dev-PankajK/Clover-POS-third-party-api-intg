# uknomi_pos_integration
Integrating module for Clover POS

## Technology Used
* Python 3.9
* Pydantic (For data serialization)
* Pytest for unit testing
* AWS CLI and AWS SAM


## Clover Connector Guidelines:

1. sam app contain 2 lambda function
    * order-reformer(This lambda function transforms the orders and send it to example api as soon as the order is created in clover POS)
    * menu-extractor - Lambda function to get menu items from Clover and update them into DynamoDB table
2. sam deploy --guided to deploy the app using template.yaml


------------------- For testing purposes I have imported default menu items from menus.csv to DynamoDB database(Note: DynamoDB table already created using sam template( Used table name is "MENU_TABLE"))-------------------

3. For testing open Windows Powershell or terminal in case of unix os and run below commands
    * pip install boto3/pip3 install boto3
    * python3 ./database.py(To import items from menu.csv to "MENU_TABLE")

## Webhook registration in clover app

To receive live events from clover, register the endpoint of order-reformer lambda function  in the clover app. To do so follow the below steps:
* open the aws stack app using AWS console which you have install using the sam template.
* Go to order-reform function and get the api endpoint to trigger lambda function.

* Now follow the steps mentioned in the video to register the endpoint, [click here](https://youtu.be/qLayueT-6-4) to watch the video.

* After successful webhook registration you can test lambda function using clover order apis. You can use the below steps to know how the lambda function is behaving on different requests
  * Use Clover order api to create some demo orders and check whether lambda function(order-reformer) executing or not.You can view function log  in cloud watch to see the execution result of order-reformer function.
  * You can also use the postman collection of clover apis which I've created for demo purposes.


## [click here]() to read the detailed documentation on clover connector



## Demo video of current workflow

* [click here](https://youtu.be/zAWhlv5yCGw) to watch the video 



