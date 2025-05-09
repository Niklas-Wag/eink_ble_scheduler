import asyncio
from flask import Blueprint, jsonify, request
from src.ble_manager import BLEManager
from src.db_manager import DatabaseManager
from src.job_manager.scheduler import JobScheduler

api_bp = Blueprint('api', __name__)
db_manager = DatabaseManager()
ble_manager = BLEManager()
job_scheduler = JobScheduler()

@api_bp.route('/displays', methods=['GET'])
def get_displays():
    displays = db_manager.get_displays()
    return jsonify(displays)

@api_bp.route('/reload', methods=['POST'])
def reload_devices():
    devices = asyncio.run(ble_manager.scan_for_devices())
    for device_name in devices:
        db_manager.add_device(device_name.name, device_name.address)
    return jsonify({'status': 'success'})

@api_bp.route('/displays/<string:device_name>', methods=['POST'])
def add_task(device_name):
    task_type = request.args.get('task')
    schedule = request.args.get('schedule')
    db_manager.schedule_task(device_name=device_name, task_type=task_type, schedule=schedule, job_scheduler=job_scheduler)
    return jsonify({'status': 'success'})

@api_bp.route('/displays/<string:device_name>', methods=['DELETE'])
def delete_display(device_name):
    db_manager.delete_device(device_name)
    return jsonify({'status': 'success'})

@api_bp.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db_manager.clear_task(task_id, job_scheduler=job_scheduler)
    return jsonify({'status': 'success'})