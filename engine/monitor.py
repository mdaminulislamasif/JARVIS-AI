import psutil

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else 100
    return {"cpu": cpu_usage, "ram": ram_usage, "battery": battery_percent}
