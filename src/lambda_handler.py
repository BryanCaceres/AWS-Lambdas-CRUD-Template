import awsgi
from .app import app
from aws_lambda_powertools import Tracer, Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit

tracer = Tracer()
logger = Logger()
metrics = Metrics()

@tracer.capture_lambda_handler
@metrics.log_metrics
@logger.inject_lambda_context
def lambda_handler(event, context):
    try:
        metrics.add_metric(name="api_requests", unit=MetricUnit.Count, value=1)
        
        if context.get("cold_start", True):
            logger.info("Cold start detected")
            metrics.add_metric(name="cold_starts", unit=MetricUnit.Count, value=1)

        response = awsgi.response(app, event, context)
        return response
    except Exception as e:
        metrics.add_metric(name="api_errors", unit=MetricUnit.Count, value=1)
        logger.error(f"Error procesando request: {e}")
        raise