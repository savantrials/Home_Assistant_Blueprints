# Home Assistant Blueprints

Automation blueprints for Home Assistant. Click a badge to import that blueprint into your Home Assistant instance.

| Blueprint | What it does | Min HA version | Import |
| --- | --- | --- | --- |
| [Everyone Leaves Lights Climate And Security Notification](everyone_is_gone/) | When everyone leaves, turns off lights, optionally sets the thermostat, and notifies about unlocked locks or open garage doors. | 2026.4.0 | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/everyone_is_gone/everyoneisgone.yaml) |
| [Family Room Lamp](family_room_lamp/) | Turns off a lamp after the TV goes off and motion has been clear for a set time. | — | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/family_room_lamp/Family_Room_Lamp.yaml) |
| [Garage Light](garage_light/) | Turns a garage light on from a door contact or motion sensor and off after the door closes and motion clears. | 2026.5.0 | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/garage_light/Garage_Light.yaml) |
| [Garbage Disposal Pico](garbage_disposal_pico/) | Turns an outlet or switch on and off from a Lutron Pico remote's on and off buttons. | 2026.5.2 | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/garbage_disposal_pico/Garbage_Disposal_Pico.yaml) |
| [Hallway Light 2](hallway_light_2/) | Motion-activated hallway light with blocking sensor, blocking light, and time window conditions, plus optional switches, scenes, and scripts. | — | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/hallway_light_2/Hallway_Light_2.yaml) |
| [Master Bathroom Lights](master_bathroom_lights/) | Motion-activated lights with per-period brightness (morning, day, evening, night) and door sensors that hold the lights on. | 2026.5.1 | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/savantrials/Home_Assistant_Blueprints/refs/heads/main/master_bathroom_lights/Master_Bathroom_Lights.yaml) |

## Checks

Every push and pull request runs [`scripts/check_blueprints.py`](scripts/check_blueprints.py), which:

- parses every `.yaml` file (Home Assistant tags like `!input` are allowed) and checks each blueprint has a `name` and `domain`;
- checks that every import badge link in a Markdown file points to a blueprint file that exists in this repo (paths are case-sensitive);
- checks that every blueprint has an import badge in this README and in its folder's README.

When you rename a blueprint file, update the badge URL in both READMEs in the same commit. Run the checks locally with:

```sh
pip install pyyaml
python scripts/check_blueprints.py
```
