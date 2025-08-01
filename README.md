# NEO NAS-AB02B2 Zigbee Siren MQTT Control

**Reliable melody control for NEO NAS-AB02B2 Zigbee sirens via MQTT**

## The Problem

The NEO NAS-AB02B2 Zigbee siren has a significant limitation when controlled through Home Assistant's standard entity controls:

- **Melody changes are unreliable** when sent together with alarm activation
- Standard HA siren entity controls often fail to change melodies
- The device doesn't respond correctly to combined `{"alarm": true, "melody": X}` payloads
- This makes it impossible to create reliable doorbell vs alarm scenarios

## Working Pattern:
1. **Set melody + volume**: `{"melody": 18, "volume": "low"}`
2. **Wait 2-3 seconds** for device to process the configuration
3. **Trigger alarm**: `{"alarm": true}`
4. **Stop when done**: `{"alarm": false}`

**Key insight**: The device remembers the melody/volume setting until explicitly changed. You must separate configuration from activation.

## Available Melodies

The NEO NAS-AB02B2 supports 18 built-in melodies but these four are useful for testing, validation and common alarming use-cases (break in alerting, smoke alarms, doorbells, etc). 

Respectively:

| Melody | Name | Suggested Use |
|--------|------|---------------|
| 6 | **Alarm** | **Security alarms** |
| 12 | **Chime** | **Gentle notifications** |
| 15 | **Clock Chime** | **Time notifications** |
| 18 | **Ding Dong** | **Doorbell (recommended)** |


**Volume levels**: `"low"`, `"medium"`, `"high"`

## 🐍 Python Testing Scripts

### Basic Test Script

```python
#!/usr/bin/env python3
"""
Test NEO NAS-AB02B2 siren with separated commands
"""
import paho.mqtt.client as mqtt
import json
import time

def send_command(device_name, payload):
    client = mqtt.Client()
    client.username_pw_set("your_mqtt_user", "your_mqtt_password")
    client.connect("your_mqtt_broker", 1883, 60)
    
    topic = f"zigbee2mqtt/{device_name}/set"
    client.publish(topic, json.dumps(payload))
    client.disconnect()

def test_doorbell(siren_name):
    """Test doorbell scenario with melody 18"""
    print("🔧 Setting doorbell melody...")
    send_command(siren_name, {"melody": 18, "volume": "medium"})
    
    print("⏰ Waiting 3 seconds...")
    time.sleep(3)
    
    print("🔔 Triggering doorbell...")
    send_command(siren_name, {"alarm": True})
    
    print("🎵 Playing for 5 seconds...")
    time.sleep(5)
    
    print("🛑 Stopping...")
    send_command(siren_name, {"alarm": False})

# Usage
test_doorbell("office_siren")
```

## 🏠 Home Assistant Integration

### Dedicated Scenario Scripts

Add these to your `configuration.yaml` under `script:`:

```yaml
script:
  # Doorbell - Melody 18 (Ding Dong)
  doorbell_activate:
    alias: "Activate Doorbell"
    sequence:
      # Configure all sirens for doorbell
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"melody": 18, "volume": "medium"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"melody": 18, "volume": "medium"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/bedroom_siren/set"
          payload: '{"melody": 18, "volume": "low"}'
      # Add your other sirens here
      
      # Wait for configuration
      - delay:
          seconds: 3
          
      # Trigger doorbell
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/bedroom_siren/set"
          payload: '{"alarm": true}'
      
      # Auto-stop after 5 seconds
      - delay:
          seconds: 5
      - service: script.sirens_stop

  # Security Alarm - Melody 6 (Alarm)
  security_alarm_activate:
    alias: "Activate Security Alarm"
    sequence:
      # Configure all sirens for alarm
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"melody": 6, "volume": "high"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"melody": 6, "volume": "high"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/bedroom_siren/set"
          payload: '{"melody": 6, "volume": "high"}'
      
      # Wait for configuration
      - delay:
          seconds: 3
          
      # Trigger alarm (no auto-stop for security)
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/bedroom_siren/set"
          payload: '{"alarm": true}'

  # Gentle Notification - Melody 12 (Chime)
  gentle_notification_activate:
    alias: "Activate Gentle Notification"
    sequence:
      # Configure sirens for gentle chime
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"melody": 12, "volume": "low"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"melody": 12, "volume": "low"}'
      
      # Wait for configuration
      - delay:
          seconds: 3
          
      # Trigger gentle notification
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"alarm": true}'
      
      # Auto-stop after 8 seconds
      - delay:
          seconds: 8
      - service: script.sirens_stop

  # Clock Chime - Melody 15 (Clock Chime)
  clock_chime_activate:
    alias: "Activate Clock Chime"
    sequence:
      # Configure for clock chime
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"melody": 15, "volume": "low"}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"melody": 15, "volume": "low"}'
      
      # Wait for configuration
      - delay:
          seconds: 3
          
      # Trigger clock chime
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"alarm": true}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"alarm": true}'
      
      # Auto-stop after 6 seconds
      - delay:
          seconds: 6
      - service: script.sirens_stop

  # Stop All Sirens
  sirens_stop:
    alias: "Stop All Sirens"
    sequence:
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_siren/set"
          payload: '{"alarm": false}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/office_siren/set"
          payload: '{"alarm": false}'
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/bedroom_siren/set"
          payload: '{"alarm": false}'
      # Add your other sirens here
```

### Usage in Automations

Now you can easily use these in automations without any parameters:

```yaml
automation:
  # Doorbell pressed
  - alias: "Doorbell Pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_button
        to: "on"
    action:
      - service: script.doorbell_activate

  # Security system triggered
  - alias: "Security Breach"
    trigger:
      - platform: state
        entity_id: alarm_control_panel.home_alarm
        to: "triggered"
    action:
      - service: script.security_alarm_activate

  # Hourly time chime
  - alias: "Hourly Chime"
    trigger:
      - platform: time_pattern
        minutes: 0
    condition:
      - condition: time
        after: "08:00:00"
        before: "22:00:00"
    action:
      - service: script.clock_chime_activate

  # Gentle notification for important events
  - alias: "Laundry Done"
    trigger:
      - platform: state
        entity_id: sensor.washing_machine
        to: "finished"
    action:
      - service: script.gentle_notification_activate

  # Emergency stop (e.g., from dashboard button)
  - alias: "Emergency Stop Sirens"
    trigger:
      - platform: state
        entity_id: input_button.stop_sirens
        to: "on"
    action:
      - service: script.sirens_stop
```

### Dashboard Controls

Add these to your Lovelace dashboard:

```yaml
type: entities
title: Siren Controls
entities:
  - entity: script.doorbell_activate
    name: "🔔 Doorbell"
    tap_action:
      action: call-service
      service: script.doorbell_activate
  - entity: script.gentle_notification_activate
    name: "🔔 Gentle Chime"
    tap_action:
      action: call-service
      service: script.gentle_notification_activate
  - entity: script.clock_chime_activate
    name: "🕐 Clock Chime"
    tap_action:
      action: call-service
      service: script.clock_chime_activate
  - entity: script.security_alarm_activate
    name: "🚨 Security Alarm"
    tap_action:
      action: call-service
      service: script.security_alarm_activate
  - entity: script.sirens_stop
    name: "🛑 STOP ALL"
    tap_action:
      action: call-service
      service: script.sirens_stop
```

## 🔧 Configuration Steps

1. **Update siren device names** in the scripts to match your Zigbee2MQTT device names
2. **Add/remove sirens** as needed in each script
3. **Adjust volumes** per room (e.g., bedroom = "low", living areas = "medium")
4. **Test each script** individually before using in automations
5. **Add emergency stop** buttons to your dashboard

## ⚡ Key Benefits

- **100% reliable melody changes** using separated commands
- **No parameters needed** - each script is purpose-built
- **Easy automation integration** - just call the script
- **Consistent timing** - built-in delays ensure proper device response
- **Emergency stop** - immediate silence for all sirens

## 🛠️ Troubleshooting

**Melody doesn't change:**
- Ensure 3-second delay between configuration and trigger
- Check MQTT topic names match your Zigbee2MQTT setup
- Verify device is responsive to basic on/off commands

**Siren doesn't stop:**
- Use the emergency stop script: `script.sirens_stop`
- Check MQTT broker connectivity
- Manually send `{"alarm": false}` via MQTT

**Volume too loud/quiet:**
- Adjust volume in each script: `"low"`, `"medium"`, `"high"`
- Consider different volumes per room (bedroom = low, etc.)

## 📋 Device Requirements

- NEO NAS-AB02B2 Zigbee siren
- Zigbee2MQTT integration in Home Assistant
- MQTT broker (Mosquitto recommended)
- Home Assistant with MQTT integration enabled

