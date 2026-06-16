from bleak.exc import BleakError

DOMAIN = "ac_infinity_airtap"

MANUFACTURER = "AC Infinity"

DEVICE_TIMEOUT = 30
# Poll interval is controlled by _MIN_SECONDS_BETWEEN_POLLS in device.py

BLEAK_EXCEPTIONS = (AttributeError, BleakError, TimeoutError)

DEVICE_MODEL = {1: "Controller 67",
                6: "Airtap Series",
                7: "Controller 69",
                11: "Controller 69 Pro"}


def get_device_model(device_type: int) -> str:
    return DEVICE_MODEL.get(device_type, f"AC Infinity Device (type {device_type})")

FAMILY_E_MODELS = {7, 9, 11, 12}
