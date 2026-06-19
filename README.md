Deep thoughts on the AC Infinity Airtap

There are 4 known versions of this device.  Look on the back of the unit on the fan box for hints to your model.

"Gen 0" - Mine was purchased in mid 2023, no smart features or remote.  No FCC ID as it does not transmit signals. No "Gen" lsited after the mode name.

"Gen 1" - Smart features with app and BT connectivity.  Now with FCC ID: 2AXMF-RBF.  May not be compatible with these HA integrations.  No "Gen" listed after the model name.

"Gen 2" - Smart features with app and BT connectivity.  "Gen 2" listed after the model name.  Compatible with these BT HA integrations.

"Gen 3" - Smart features with app and BT connectivity.  Latest available, same FCC ID as above. "Gen 3" text after model name.  Purchased mine 5/2026.

# Vibecoded 6.18.26 for customizations/optimization
Here's the full changelog from the original upload (v1.1.1) to the current build (v1.1.3):

---

**`manifest.json`**
- Bumped version from `1.1.1` to `1.1.3`
- `"domain"` changed from `"ac_infinity"` to `"ac_infinity_airtap"`

**`const.py`**
- `DOMAIN` changed from `"ac_infinity"` to `"ac_infinity_airtap"`
- Removed unused `UPDATE_SECONDS = 15` constant
- Added `get_device_model(device_type: int) -> str` helper function with safe `.get()` fallback for unknown device types

**`device.py`**
- `set_mode_auto`: removed duplicate `await self._ensure_connected()` call that appeared before the `try` block
- `async_set_max_speed`: fixed copy-paste bug where `self.state.level_off = value` was incorrectly used instead of `self.state.level_on = value`

**`fan.py`**
- Imports updated to include `get_device_model` and `WORK_TYPE_ON`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`
- Added `PRESET_AUTO_MODE = "Auto"` and `PRESET_ON_MODE = "On"` preset constants
- Preset list set to `[Auto, On]`
- Added `is_on` property override to prevent base `FanEntity` class from overriding `_attr_is_on`
- `async_set_preset_mode`: `Auto` calls `set_mode_auto()`, `On` calls `turn_on(None)`
- `_update_attrs`: refactored into three explicit states driven by `work_type`:
  - `WORK_TYPE_AUTO` → `preset_mode = "Auto"`, `is_on` and `percentage` only set to active values when `fan_speed > 1`; otherwise `is_on = False` and `percentage = 0` to prevent icon spinning when fan idles in auto mode
  - `WORK_TYPE_ON` → `is_on = True`, `preset_mode = "On"`, live percentage
  - `WORK_TYPE_OFF` → `is_on = False`, `preset_mode = None`, `percentage = 0`

**`number.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**`sensor.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**`switch.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**Component folder**
- Renamed from `custom_components/ac_infinity/` to `custom_components/ac_infinity_airtap/`

**`brand/` (new)**
- Renamed from `images/` to `brand/` — correct folder name for HACS and HA integrations UI
- Contains `icon.png` (256×256px) and `logo.png`

**`hacs.json`**
- Added `"icon"` field pointing to `custom_components/ac_infinity_airtap/brand/icon.png`

**Unchanged:** `__init__.py`, `config_flow.py`, `coordinator.py`, `models.py`, `strings.json`, `translations/en.json`

---

Home Assistant custom integration for Bluetooth Low Energy (BLE) control of [AC Infinity Airtap](https://acinfinity.com/register-booster-fans/) series register fans.

Uses [ac-infinity-ble](https://github.com/hunterjm/ac-infinity-ble/) library.

## Troubleshooting

### Debug Logging

To enbale debug logging, configure the your [loggers](https://www.home-assistant.io/integrations/logger/) as follows:

```yaml
logger:
  default: info
  logs:
    ac_infinity_ble: debug
    custom_components.ac_infinity: debug
```

## Credit

This project builds on work by Jason Hunter: [hunterjm/ac-infinity-hacs](https://github.com/hunterjm/ac-infinity-hacs)
and mtsphere: https://github.com/mtsphere/ac-infinity-airtap-hacs
