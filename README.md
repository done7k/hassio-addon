# Welcome to GitHub

Collection of addons for Home Assistant

## konnected board status to Home Assistant

The program is designed for Home Assistant. 

konnected board maintains a tiny webserver and can returns a set of configuration and status values. In some installation environments it is critical to see board level of Wifi signal which is not provided by standard konnected integration. This addon fetches “/status” information including RSSI strength; adds proper icon name and returns indormaiton in JSON format. Running it as a sensor gives you real-time connection status for your konnected board in Home Assistant.

![repo-settings-image](https://github.com/done7k/hassio-addon/blob/master/images/konnekted_card.PNG)

![repo-settings-image](https://github.com/done7k/hassio-addon/blob/master/images/konnekted_sensor.PNG)

### Installation

1. Move the "konnected_board_check.py" program to /config/custom_components forder on HA ;

2. Configure a new sensor in your configuration.yaml file (replace IP address and port for your board)
```
sensor: 
 - platform: command_line
    name: Konnected_board_A
    command: "python3 /config/custom_components/konnected_board_check.py http://192.168.200.200:1234/status"
    scan_interval: 300
    command_timeout: 20
    json_attributes:
      - hwVersion
      - swVersion
      - ip
      - rssi
      - uptime
      - error
      - device_class # device_class: signal_strength
      - icon
      - unit_of_measurement
    value_template: '{{ value_json.rssi }}'
```

3. restart your HA

Additionally, you can configure automation to report connection lost and/or resume cases. In automation.yaml file:
``` 
- id: Konnected_panel_A_availability
  alias: Konnected_panel_A_unavilable
  trigger:
  - platform: state
    entity_id: sensor.konnected_board_a
    to: "unavailable"
  action:
  - service: notify.notify
    data_template:
      message: "Konnected panel A unavalable! Error: {{ state_attr('sensor.konnected_board_a', 'error') }} "

- id: Konnected_panel_A_availability_back
  alias: Konnected_panel_A_available
  trigger:
  - platform: state
    entity_id: sensor.konnected_board_a
    from: "unavailable"
  action:
  - service: notify.notify
    data_template:
      message: "Konnected panel A is back! RSSI {{ states('sensor.konnected_board_a') }}. 
        it was off for {{ state_attr('sensor.konnected_board_a_unavailable_last_hour', 'value') }} last hour 
        and {{ state_attr('sensor.konnected_board_a_unavailable_24hrs', 'value') }} last 24h.
        Board uptme {{ (state_attr('sensor.konnected_board_a', 'uptime') | int) | timestamp_custom('%H:%M:%S', 0) }}"

```
