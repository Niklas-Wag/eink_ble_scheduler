from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .weather_job import WeatherJob

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}

    def schedule_job(self, device_name, cron_schedule):
        job = WeatherJob(device_name)
        job_id = f"{device_name}_job"
        self.jobs[device_name] = self.scheduler.add_job(job.execute, CronTrigger.from_crontab(cron_schedule), id=job_id)
        job.execute()

    def remove_job(self, device_name):
        job_id = f"{device_name}_job"
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[device_name]

    def load_jobs(self):
        from src.db_manager import DatabaseManager
        db_manager = DatabaseManager()
        devices = db_manager.get_displays()
        for device in devices:
            if device['task']:
                self.schedule_job(device['name'], device['task']['schedule'])

    def start(self):
        self.load_jobs()
        self.scheduler.start()