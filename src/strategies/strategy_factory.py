
from src.strategies.utils.s3_utils import S3Utils
from src.strategies.utils.dynamodb_utils import DynamoDBUtils
from src.strategies.workflow.s3_remove_pii import S3RemovePii
from common.logger import Logger


LOGGER=Logger(__name__)
VALID_FACTORY_STRATEGIES = [
    's3_remove_pii',
    's3_utils',
    'dynamodb_utils',
]


class StrategyFactory:
    def __init__(self, event):
        self.event = event
        if not self._validate_strategy(self.event):
            raise Exception("Event must contain 'request_type'")
        self._initiate_strategy(self.event.get("request_type"))
        self._strategy.handle(self.event)


    def _validate_strategy(self):
        if self.event and \
            self.event.get("request_type") in VALID_FACTORY_STRATEGIES:
            LOGGER.info(f'Valid strategy {self.event.get("request_type")} found')
            return True
        return False

    def _initiate_strategy(self,strategy_name):
        strategy_class = globals().get(strategy_name)
        self._strategy= strategy_class(self.event)
        LOGGER.info(f'Initialized strategy: {self.request_type}')   




