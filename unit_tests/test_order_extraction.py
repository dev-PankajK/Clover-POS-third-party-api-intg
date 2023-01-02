from order_reformer_function import app

def test_lambda_handler():
    event = {
        "httpMethod":"POST",
        "body":'{"order_ids_list":["ok"]}'
    }
    assert app.lambda_handler(event, None) == {'body': '"ok"', 'statusCode': 200}

