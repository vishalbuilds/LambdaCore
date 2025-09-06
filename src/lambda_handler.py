from strategies.strategy_factory import StrategyFactory
from common.response_builder import ResponseBuilder
from common.event_sanitizer import EventSanitizer
from common.logger import Logger

LOGGER = Logger(__name__)

def lambda_handler(event, context):
    LOGGER.info(f"Lambda handler started with {event}.")
    # Sanitize incoming event dictionary
    sanitizer = EventSanitizer(event)
    clean_event = sanitizer.data  # get sanitized dictionary
    print(clean_event)
    
    LOGGER.info(f"Received event: {clean_event}")
    
    # Use StrategyFactory to choose and run strategy
    strategy = StrategyFactory(clean_event)
    response = strategy.execute()
    LOGGER.info(f"Strategy response: {response}")
    
    # Build final Lambda response
    final_response = ResponseBuilder(result="success", data=response)
    LOGGER.info(f"Final response: {final_response}")
    
    return final_response
