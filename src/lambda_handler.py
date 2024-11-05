import awsgi
from app import app
import logging

def lambda_handler(event, context):
    logging.info(f"Layer version: {context.layer_version_arn}")
    return awsgi.response(app, event, context)