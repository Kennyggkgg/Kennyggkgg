# Dynamic commands that Ella can modify or add to
# ella_commands.py

# Core Ella Commands
def get_weather():
    location = input("Which location would you like the weather report for? ")
    report = ella_instance.fetch_weather_report(location)
    return f"Weather in {location}: {report}"

def play_music():
    song = input("Which song or genre would you like to listen to? ")
    ella_instance.play_song(song)
    return f"Now playing {song}."

def control_smart_home():
    device = input("Which smart home device would you like to control? ")
    action = input(f"What should I do with the {device}? (e.g., turn on/off) ")
    ella_instance.control_device(device, action)
    return f"Smart home action '{action}' executed on {device}."

def create_shopping_list():
    items = input("What items would you like to add to the shopping list? ")
    ella_instance.add_to_shopping_list(items)
    return f"Added {items} to your shopping list."

def check_flight_status():
    flight_number = input("What is the flight number? ")
    status = ella_instance.get_flight_status(flight_number)
    return f"Flight {flight_number} status: {status}."

def daily_summary():
    summary = ella_instance.get_daily_summary()
    return f"Here is your daily summary: {summary}"

def check_stocks():
    stock_symbol = input("Which stock would you like to check? ")
    stock_price = ella_instance.get_stock_price(stock_symbol)
    return f"Current price of {stock_symbol}: {stock_price}"


# Hack-Specific Commands
def scan_network():
    print("Scanning local network for connected devices...")
    devices = hack_instance.network_scan()
    return f"Found {len(devices)} devices on the network."

def intercept_bluetooth():
    print("Scanning for nearby Bluetooth devices...")
    devices = hack_instance.bluetooth_scan()
    return f"Bluetooth scan complete. Found {len(devices)} devices."

def hack_camera():
    print("Hacking nearby camera feeds...")
    feeds = hack_instance.hack_camera_feeds()
    return f"Hacked {len(feeds)} camera feeds. Streaming live."

def security_breach_alert():
    hack_instance.detect_security_breach()
    send_security_email()
    return "Security breach detected. Alert email sent."

def encrypt_communication():
    hack_instance.encrypt_all_communications()
    return "All communications are now encrypted."

def track_user_location():
    locations = hack_instance.track_device_locations()
    return f"Tracking locations of {len(locations)} users."

def disable_intruder_device():
    success = hack_instance.disable_device()
    return "Intruder device disabled." if success else "Failed to disable intruder device."

def hijack_fm_signal():
    hack_instance.hijack_signal()
    return "FM signal hijacked and broadcasting your message."

def disable_intruder_network():
    hack_instance.disable_network_access_for_intruder()
    return "Intruder's network access disabled."

def setup_security_trap():
    hack_instance.activate_security_trap()
    return "Security trap activated."

def track_anomalies():
    anomalies = hack_instance.monitor_network_anomalies()
    return f"{len(anomalies)} anomalies detected and logged."