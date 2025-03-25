from src.job_manager.base_job import BaseJob
from src.logging_config import logger

class WeatherJob(BaseJob):
    def execute(self):
        logger.info(f"Executing job for device: {self.device_name}")
        # Add the job logic here