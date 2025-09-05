from src.strategies.strategy_factory import StrategyFactory
from src.common.response_builder import ResponseBuilder
from src.common import event_sanitizer


def lambda_handler(event, context):
   
    clean_event = event_sanitizer(event) 
    request_type = clean_event.get('request_type')
    response = StrategyFactory(clean_event)

    return ResponseBuilder(result="success", data=response)
