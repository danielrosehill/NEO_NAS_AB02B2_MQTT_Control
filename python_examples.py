#!/usr/bin/env python3
"""
NEO NAS-AB02B2 Zigbee Siren - Python MQTT Control Examples
Demonstrates the separated command approach for reliable melody control
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime


class NEOSirenController:
    """Controller for NEO NAS-AB02B2 Zigbee sirens via MQTT"""
    
    def __init__(self, mqtt_host="localhost", mqtt_port=1883, 
                 username=None, password=None):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.username = username
        self.password = password
        
        # Your siren device names (update these to match your setup)
        self.sirens = [
            "living_room_siren",
            "office_siren", 
            "bedroom_siren",
            "kitchen_siren"
        ]

    def send_command(self, device_name: str, payload: dict, description: str = ""):
        """Send MQTT command to a specific siren"""
        client = mqtt.Client()
        
        if self.username and self.password:
            client.username_pw_set(self.username, self.password)
        
        try:
            client.connect(self.mqtt_host, self.mqtt_port, 60)
            topic = f"zigbee2mqtt/{device_name}/set"
            payload_json = json.dumps(payload)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] 📤 {device_name}: {description}")
            print(f"           ✅ Sent: {payload_json}")
            
            result = client.publish(topic, payload_json)
            client.disconnect()
            return result.rc == mqtt.MQTT_ERR_SUCCESS
                
        except Exception as e:
            print(f"           ❌ Error: {e}")
            return False

    def configure_sirens(self, melody: int, volume: str = "medium", 
                        sirens: list = None):
        """Configure melody and volume on specified sirens"""
        if sirens is None:
            sirens = self.sirens
            
        print(f"🔧 Configuring {len(sirens)} siren(s)")
        print(f"   Melody: {melody}, Volume: {volume}")
        
        for siren in sirens:
            self.send_command(siren, {"melody": melody, "volume": volume}, 
                            f"Set melody {melody}, volume {volume}")

    def trigger_sirens(self, sirens: list = None):
        """Trigger alarms on specified sirens"""
        if sirens is None:
            sirens = self.sirens
            
        print(f"🔔 Triggering {len(sirens)} siren(s)")
        for siren in sirens:
            self.send_command(siren, {"alarm": True}, "Start alarm")

    def stop_sirens(self, sirens: list = None):
        """Stop alarms on specified sirens"""
        if sirens is None:
            sirens = self.sirens
            
        print(f"🛑 Stopping {len(sirens)} siren(s)")
        for siren in sirens:
            self.send_command(siren, {"alarm": False}, "Stop alarm")

    # Dedicated scenario methods
    def doorbell_activate(self):
        """Activate doorbell on all sirens (Melody 18 - Ding Dong)"""
        print("\n🔔 DOORBELL SCENARIO")
        print("=" * 50)
        
        # Step 1: Configure for doorbell
        self.configure_sirens(melody=18, volume="medium")
        
        # Step 2: Wait for configuration
        print("⏰ Waiting 3 seconds for configuration...")
        time.sleep(3)
        
        # Step 3: Trigger doorbell
        self.trigger_sirens()
        
        # Step 4: Auto-stop after 5 seconds
        print("🎵 Playing doorbell for 5 seconds...")
        time.sleep(5)
        
        self.stop_sirens()
        print("✅ Doorbell completed")

    def security_alarm_activate(self):
        """Activate security alarm on all sirens (Melody 6 - Alarm)"""
        print("\n🚨 SECURITY ALARM SCENARIO")
        print("=" * 50)
        
        # Step 1: Configure for alarm
        self.configure_sirens(melody=6, volume="high")
        
        # Step 2: Wait for configuration
        print("⏰ Waiting 3 seconds for configuration...")
        time.sleep(3)
        
        # Step 3: Trigger alarm (no auto-stop for security)
        self.trigger_sirens()
        
        print("🚨 Security alarm ACTIVE - manual stop required!")
        print("💡 Use stop_sirens() method to stop")

    def gentle_notification_activate(self, duration: int = 8):
        """Activate gentle notification (Melody 12 - Chime)"""
        print("\n🔔 GENTLE NOTIFICATION SCENARIO")
        print("=" * 50)
        
        # Step 1: Configure for gentle chime
        self.configure_sirens(melody=12, volume="low")
        
        # Step 2: Wait for configuration
        print("⏰ Waiting 3 seconds for configuration...")
        time.sleep(3)
        
        # Step 3: Trigger gentle notification
        self.trigger_sirens()
        
        # Step 4: Auto-stop after specified duration
        print(f"🎵 Playing gentle chime for {duration} seconds...")
        time.sleep(duration)
        
        self.stop_sirens()
        print("✅ Gentle notification completed")

    def clock_chime_activate(self, duration: int = 6):
        """Activate clock chime (Melody 15 - Clock Chime)"""
        print("\n🕐 CLOCK CHIME SCENARIO")
        print("=" * 50)
        
        # Step 1: Configure for clock chime
        self.configure_sirens(melody=15, volume="low")
        
        # Step 2: Wait for configuration
        print("⏰ Waiting 3 seconds for configuration...")
        time.sleep(3)
        
        # Step 3: Trigger clock chime
        self.trigger_sirens()
        
        # Step 4: Auto-stop after specified duration
        print(f"🎵 Playing clock chime for {duration} seconds...")
        time.sleep(duration)
        
        self.stop_sirens()
        print("✅ Clock chime completed")

    def emergency_stop(self):
        """Emergency stop all sirens immediately"""
        print("\n🚨 EMERGENCY STOP")
        print("=" * 50)
        self.stop_sirens()
        print("✅ All sirens stopped")


def main():
    """Example usage of the NEO siren controller"""
    
    # Initialize controller with your MQTT settings
    controller = NEOSirenController(
        mqtt_host="10.0.0.4",  # Your MQTT broker IP
        mqtt_port=1883,
        username="homeassistant",  # Your MQTT username
        password="your_password"   # Your MQTT password
    )
    
    try:
        print("🎯 NEO NAS-AB02B2 Siren Controller Demo")
        print("=" * 60)
        
        # Test doorbell
        controller.doorbell_activate()
        
        print("\n" + "="*60)
        input("Press Enter to test gentle notification...")
        
        # Test gentle notification
        controller.gentle_notification_activate()
        
        print("\n" + "="*60)
        input("Press Enter to test clock chime...")
        
        # Test clock chime
        controller.clock_chime_activate()
        
        print("\n" + "="*60)
        response = input("Test security alarm? (y/N): ")
        if response.lower() == 'y':
            controller.security_alarm_activate()
            input("Press Enter to stop security alarm...")
            controller.emergency_stop()
        
        print("\n🎉 Demo completed!")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted - stopping all sirens...")
        controller.emergency_stop()


# Individual test functions for quick testing
def test_doorbell():
    """Quick doorbell test"""
    controller = NEOSirenController(
        mqtt_host="10.0.0.4",
        username="homeassistant", 
        password="your_password"
    )
    controller.doorbell_activate()


def test_gentle_chime():
    """Quick gentle chime test"""
    controller = NEOSirenController(
        mqtt_host="10.0.0.4",
        username="homeassistant",
        password="your_password"
    )
    controller.gentle_notification_activate()


def emergency_stop_all():
    """Quick emergency stop"""
    controller = NEOSirenController(
        mqtt_host="10.0.0.4",
        username="homeassistant",
        password="your_password"
    )
    controller.emergency_stop()


if __name__ == "__main__":
    main()
