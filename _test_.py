from src.lambda_handler import lambda_handler

lambda_handler({"request_type": "s3_remove_pii"}, None)

