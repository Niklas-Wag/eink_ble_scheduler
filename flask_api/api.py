import asyncio
from flask import Blueprint, jsonify, request
from ble_manager import BLEManager
from db_manager import DatabaseManager

api_bp = Blueprint('api', __name__)
db_manager = DatabaseManager()
ble_manager = BLEManager()

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([])

@api_bp.route('/displays', methods=['GET'])
def get_displays():
    devices = db_manager.get_devices()
    return jsonify([{'id': device.id, 'name': device.name} for device in devices])

@api_bp.route('/reload', methods=['POST'])
def reload_devices():
    devices = asyncio.run(ble_manager.scan_for_devices())
    for device_name in devices:
        db_manager.add_device(device_name)
    return jsonify({'status': 'success', 'devices': devices})

@api_bp.route('/displays/<string:device_id>', methods=['POST'])
def add_task(device_id):
    task_type = request.args.get('task')
    schedule = request.json.get('schedule')
    db_manager.add_scheduled_task(device_id, task_type, schedule)
    return jsonify({'status': 'success'})

@api_bp.route('/displays/<string:device_id>', methods=['DELETE'])
def delete_display(device_id):
    db_manager.delete_device(device_id)
    return jsonify({'status': 'success'})