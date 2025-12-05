from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import platform
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

def get_system_info():
    """Mengambil informasi sistem dan return sebagai dictionary"""
    
    # Informasi RAM
    ram = psutil.virtual_memory()
    ram_percent = (ram.total - ram.available) / ram.total * 100 if ram.total > 0 else 0
    
    # Informasi CPU
    cpu_freq = psutil.cpu_freq()
    
    # Informasi Storage
    disk = psutil.disk_usage('/')

    storage_used = disk.total - disk.free
    storage_free = disk.total - storage_used
    storage_percent = (disk.total - disk.free) / disk.total * 100 if disk.total > 0 else 0
    
    # Informasi System
    system_info = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "processor": platform.processor()
        },
        "hardware": {
            "ram": {
                "total_gb": round(ram.total / (1024**3), 2),
                "used_gb": round((ram.total - ram.available)/ (1024**3), 2),
                "available_gb": round(ram.available / (1024**3), 2),
                "usage_percent": ram_percent,
                #"ram": ram
            },
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "usage_percent": psutil.cpu_percent(interval=1),
                "current_frequency_mhz": round(cpu_freq.current, 2) if cpu_freq else None,
                "max_frequency_mhz": round(cpu_freq.max, 2) if cpu_freq else None
            },
            "storage": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(storage_used / (1024**3), 2),
                "free_gb": round(storage_free / (1024**3), 2),
                # "used_gb": round(disk.used / (1024**3), 2),
                #"free_gb": round(storage_free / (1024**3), 2),
                "usage_percent": storage_percent,
                #"all_info": disk
            }
        }
    }
    
    return system_info

@app.route('/')
def home():
    return """
    <h1>System Info API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/system">/api/system</a> - Full system info</li>
        <li><a href="/api/ram">/api/ram</a> - RAM info only</li>
        <li><a href="/api/cpu">/api/cpu</a> - CPU info only</li>
        <li><a href="/api/storage">/api/storage</a> - Storage info only</li>
    </ul>
    """

@app.route('/api/system', methods=['GET'])
def system_info():
    """Endpoint untuk semua informasi sistem"""
    try:
        info = get_system_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ram', methods=['GET'])
def ram_info():
    """Endpoint khusus informasi RAM"""
    try:
        ram = psutil.virtual_memory()
        info = {
            "timestamp": datetime.now().isoformat(),
            "ram": {
                "total_gb": round(ram.total / (1024**3), 2),
                "used_gb": round(ram.used / (1024**3), 2),
                "available_gb": round(ram.available / (1024**3), 2),
                "usage_percent": ram.percent
            }
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cpu', methods=['GET'])
def cpu_info():
    """Endpoint khusus informasi CPU"""
    try:
        cpu_freq = psutil.cpu_freq()
        info = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "usage_percent": psutil.cpu_percent(interval=1),
                "current_frequency_mhz": round(cpu_freq.current, 2) if cpu_freq else None,
                "max_frequency_mhz": round(cpu_freq.max, 2) if cpu_freq else None
            }
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/storage', methods=['GET'])
def storage_info():
    """Endpoint khusus informasi Storage"""
    try:
        disk = psutil.disk_usage('/')
        info = {
            "timestamp": datetime.now().isoformat(),
            "storage": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": disk.percent
            }
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting System Info API Server...")
    print("Access the API at: http://localhost:5005")
    print("Available endpoints:")
    print("  - http://localhost:5005/api/system")
    print("  - http://localhost:5005/api/ram") 
    print("  - http://localhost:5005/api/cpu")
    print("  - http://localhost:5005/api/storage")
    
    app.run(host='0.0.0.0', port=5005, debug=True)