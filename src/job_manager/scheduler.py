from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.job_manager.weather_job import WeatherJob
from src.logging_config import logger

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(job_defaults={'misfire_grace_time': 60})
        self.jobs = {}

    def schedule_job(self, device_name, cron_schedule):
        job_id = f"{device_name}_job"
        if job_id in self.jobs:
            self.remove_job(device_name)

        job = WeatherJob(device_name)
        logger.info(f"Scheduling job for device: {device_name} with cron: {cron_schedule}")

        cron_trigger = CronTrigger.from_crontab(cron_schedule)
        self.jobs[device_name] = self.scheduler.add_job(job.execute, cron_trigger, id=job_id)

        job.execute()

    def remove_job(self, device_name):
        job_id = f"{device_name}_job"
        if device_name in self.jobs:
            try:
                logger.info(f"Removing job for device: {device_name}")
                self.scheduler.remove_job(job_id)
                del self.jobs[device_name]
            except Exception as e:
                logger.error(f"Error removing job for {device_name}: {e}")

    def load_jobs(self):
        from src.db_manager import DatabaseManager

        db_manager = DatabaseManager()
        devices = db_manager.get_displays()

        for device in devices:
            task = device.get('task')
            if task:
                self.schedule_job(device['name'], task['schedule'])

    def start(self):
        logger.info("Starting JobScheduler")

        if not self.scheduler.running:
            self.scheduler.start()

        self.load_jobs()
