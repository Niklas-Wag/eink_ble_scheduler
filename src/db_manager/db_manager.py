from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    name = Column(String, primary_key=True)
    task_type = Column(String, nullable=True)
    schedule_cron = Column(String, nullable=True)
    schedule_created_at = Column(DateTime, nullable=True)

class DatabaseManager:
    def __init__(self, db_url="sqlite:///eink.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def add_device(self, name):
        session = self.get_session()
        device = session.query(Device).filter_by(name=name).first()
        if not device:
            device = Device(name=name)
            session.add(device)
            session.commit()
        session.close()

    def schedule_task(self, device_name, task_type, schedule, job_scheduler):
        session = self.get_session()
        device = session.query(Device).filter_by(name=device_name).first()
        device.task_type = task_type
        device.schedule_cron = schedule
        device.schedule_created_at = datetime.now()
        session.commit()
        job_scheduler.schedule_job(device_name, schedule)
        session.close()

    def get_displays(self):
        session = self.get_session()
        devices = session.query(Device).all()
        displays = [
            {
                "name": device.name,
                "task": {
                    "task_type": device.task_type,
                    "schedule": device.schedule_cron,
                    "created_at": device.schedule_created_at
                } if device.task_type else None
            }
            for device in devices
        ]
        session.close()
        return displays

    def delete_device(self, device_name):
        session = self.get_session()
        device = session.query(Device).get(device_name)
        if device:
            session.delete(device)
            session.commit()
        session.close()

    def clear_task(self, device_name, job_scheduler):
        session = self.get_session()
        device = session.query(Device).get(device_name)
        if device:
            device.task_type = None
            device.schedule_cron = None
            device.schedule_created_at = None
            session.commit()
            job_scheduler.remove_job(device_name)
        session.close()