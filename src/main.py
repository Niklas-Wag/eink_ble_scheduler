from flask_api import create_app
from src.job_manager.scheduler import JobScheduler

app = create_app()
job_scheduler = JobScheduler()
job_scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)


    #todo: make factory for jobs