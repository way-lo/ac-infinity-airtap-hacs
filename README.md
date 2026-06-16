# Vibecode edited 6.16.26 for corrections
Here's the full changelog comparing v1.1.1 → v1.1.2:

---

**`manifest.json`**
- Bumped version from `1.1.1` to `1.1.2`

**`const.py`**
- Removed unused `UPDATE_SECONDS = 15` constant
- Added `get_device_model(device_type: int) -> str` helper function with safe `.get()` fallback for unknown device types

**`device.py`**
- `set_mode_auto`: removed duplicate `await self._ensure_connected()` call that appeared before the `try` block
- `async_set_max_speed`: fixed copy-paste bug where `self.state.level_off = value` was incorrectly used instead of `self.state.level_on = value`

**`fan.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**`number.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**`sensor.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

**`switch.py`**
- Import updated to include `get_device_model`
- `DeviceInfo` construction: replaced `DEVICE_MODEL[device.state.type]` with `get_device_model(device.state.type)`

---

**Unchanged:** `__init__.py`, `config_flow.py`, `coordinator.py`, `fan.py` (logic), `models.py`, `strings.json`, `translations/en.json`, `hacs.json`

# ac-infinity-airtap-hacs

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

This project builds on work by Jason Hunter: [hunterjm/ac-infinity-hacs](https://github.com/hunterjm/ac-infinity-hacs).
