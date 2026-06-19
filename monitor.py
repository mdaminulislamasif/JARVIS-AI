import psutil
import speedtest
import socket

class SystemMonitor:
    def __init__(self, brain_module):
        self.brain = brain_module

    def check_internet_status(self):
        try:
            # Check if we can connect to a common server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def get_network_speed(self):
        self.brain.speak("Analyzing network speed. Please wait...")
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            res = f"Download: {download:.2f} Mbps, Upload: {upload:.2f} Mbps."
            self.brain.speak(res)
            return res
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return "Speed test failed. Check your connection."

    def report_health(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        bat_str = f"{battery.percent}%" if battery else "N/A"
        
        net_status = "ONLINE" if self.check_internet_status() else "OFFLINE"
        
        report = f"System Health: CPU {cpu}%, RAM {ram}%, Battery {bat_str}. Network Status: {net_status}."
        self.brain.speak(report)
        return report

    def get_network_info(self):
        # Get local IP and hostname
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return {"hostname": hostname, "local_ip": local_ip}
