# NEO NAS-AB02B2 YAML Scripts

Ready-to-use Home Assistant YAML scripts for NEO NAS-AB02B2 Zigbee sirens.

## 📁 Script Categories

### 🏠 Production Scripts (All 6 Sirens)
Control all sirens in your home with these scenarios:

| Scenario | Melody | On Script | Off Script |
|----------|--------|-----------|------------|
| 🔔 **Doorbell** | 12 | `doorbell_on_all.yaml` | `doorbell_off_all.yaml` |
| 🚨 **Security Alarm** | 6 | `security_alarm_on_all.yaml` | `security_alarm_off_all.yaml` |
| 🔥 **Smoke Alarm** | 9 | `smoke_alarm_on_all.yaml` | `smoke_alarm_off_all.yaml` |
| 🚨 **Red Alert** | 15 | `red_alert_on_all.yaml` | `red_alert_off_all.yaml` |

### 🧪 Testing Scripts (Office & Patio Only)
For quiet testing without disturbing the whole house:

| Scenario | Melody | On Script | Off Script |
|----------|--------|-----------|------------|
| 🔔 **Test Doorbell** | 12 | `test_doorbell_on.yaml` | `test_doorbell_off.yaml` |
| 🚨 **Test Red Alert** | 15 | `test_red_alert_on.yaml` | `test_red_alert_off.yaml` |

## 🚀 Usage

### 1. Copy to Home Assistant
Copy the script content to your `configuration.yaml` under the `script:` section:

```yaml
script:
  # Paste script content here
  doorbell_on_all:
    alias: "🔔 Doorbell ON - All Sirens"
    # ... rest of script content
```

### 2. Use in Automations
Call scripts directly without parameters:

```yaml
automation:
  - alias: "Doorbell Pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_button
        to: "on"
    action:
      - service: script.doorbell_on_all
      - delay:
          seconds: 5
      - service: script.doorbell_off_all
```

### 3. Dashboard Controls
Add buttons to your Lovelace dashboard:

```yaml
type: button
name: "🔔 Doorbell"
tap_action:
  action: call-service
  service: script.doorbell_on_all
```

## ⚙️ Configuration

**Update device names** in each script to match your Zigbee2MQTT setup:
- `living_room_siren`
- `patio_siren`
- `office_siren`
- `powderroom_siren`
- `bedroom_siren`
- `bathroom_siren`

**Adjust volumes** as needed:
- `"low"` - Quiet notifications
- `"medium"` - Normal alerts
- `"high"` - Emergency situations

## 🎵 Melody Reference

| Melody | Name | Use Case |
|--------|------|----------|
| 12 | Doorbell | Front door, visitors |
| 6 | Security Alarm | Break-ins, unauthorized access |
| 9 | Smoke Alarm | Fire, smoke detection |
| 15 | Red Alert | Emergency situations |

## 🔧 Technical Details

All scripts use the **separated command approach**:
1. **Configure** melody + volume
2. **Wait** 3 seconds for device processing
3. **Trigger** alarm = true
4. **Stop** with alarm = false

This ensures 100% reliable melody changes, overcoming Home Assistant's standard siren entity limitations.
