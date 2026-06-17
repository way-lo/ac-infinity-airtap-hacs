# Vibecode edited 6.16.26 for customizations/optimization
Here's the full changelog from the original upload (v1.1.1) to the current build (v1.1.2):

---

**`manifest.json`**
- Bumped version from `1.1.1` to `1.1.2`
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
- `_update_attrs`: replaced unreliable `self._device.is_on` (no such property in `device.py`) with explicit `work_type` comparisons using `WORK_TYPE_ON`, `WORK_TYPE_AUTO`, and `WORK_TYPE_OFF`; percentage forced to `0` and `is_on` set to `False` when off

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
- Added `"icon"` field, updated through iterations to final path: `custom_components/ac_infinity_airtap/brand/icon.png`

---

**Unchanged:** `__init__.py`, `config_flow.py`, `coordinator.py`, `models.py`, `strings.json`, `translations/en.json`

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
