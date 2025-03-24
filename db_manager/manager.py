from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    scheduled_tasks = relationship("ScheduledTask", back_populates="device")


class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    task_type = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="scheduled_tasks")


class DatabaseManager:
    def __init__(self, db_url="sqlite:///task_manager.db"):
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

    def add_scheduled_task(self, device_id, task_type, schedule):
        session = self.get_session()
        task = ScheduledTask(device_id=device_id, task_type=task_type, schedule=schedule)
        session.add(task)
        session.commit()
        session.close()

    def get_devices(self):
        session = self.get_session()
        devices = session.query(Device).all()
        session.close()
        return devices

    def delete_device(self, device_id):
        session = self.get_session()
        device = session.query(Device).get(device_id)
        if device:
            session.delete(device)
            session.commit()
        session.close()
