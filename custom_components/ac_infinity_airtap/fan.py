from __future__ import annotations

import math
from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify
from homeassistant.util.percentage import (int_states_in_range,
                                           percentage_to_ranged_value,
                                           ranged_value_to_percentage)

from .const import DEVICE_MODEL, DOMAIN, MANUFACTURER, get_device_model
from .coordinator import (ACInfinityDataUpdateCoordinator,
                          ActiveBluetoothCoordinatorEntity)
from .device import WORK_TYPE_AUTO, WORK_TYPE_ON, ACInfinityDevice
from .models import ACInfinityData

SPEED_RANGE = (1, 10)

PRESET_AUTO_MODE = "Auto"
PRESET_ON_MODE = "On"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data: ACInfinityData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ACInfinityFan(data.coordinator, data.device, "Fan")])


class ACInfinityFan(
    ActiveBluetoothCoordinatorEntity[ACInfinityDataUpdateCoordinator], FanEntity
):
    _attr_has_entity_name = True
    _attr_speed_count = int_states_in_range(SPEED_RANGE)
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.PRESET_MODE
    )
    _attr_preset_modes = [PRESET_AUTO_MODE, PRESET_ON_MODE]

    def __init__(
        self,
        coordinator: ACInfinityDataUpdateCoordinator,
        device: ACInfinityDevice,
        name: str,
    ) -> None:
        super().__init__(coordinator)
        self._device = device
        self._attr_name = name
        self._attr_unique_id = f"{self._device.address}_{slugify(name)}"
        self._attr_device_info = DeviceInfo(
            name=device.name,
            model=get_device_model(device.state.type),
            manufacturer=MANUFACTURER,
            sw_version=device.state.version,
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
        )

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        speed = 0
        if percentage > 0:
            speed = math.ceil(percentage_to_ranged_value(SPEED_RANGE, percentage))

        await self._device.set_speed(speed)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        if preset_mode is not None:
            await self.async_set_preset_mode(preset_mode)
            return
        speed = None
        if percentage is not None:
            speed = math.ceil(percentage_to_ranged_value(SPEED_RANGE, percentage))
        await self._device.turn_on(speed)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._device.turn_off()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode == PRESET_AUTO_MODE:
            await self._device.set_mode_auto()
        elif preset_mode == PRESET_ON_MODE:
            await self._device.turn_on(None)
        else:
            raise ValueError(f"Unsupported preset mode: {preset_mode}")

    @callback
    def _update_attrs(self) -> None:
        """Handle updating _attr values."""
        work_type = self._device.state.work_type
        fan_speed = self._device.state.fan

        if work_type == WORK_TYPE_AUTO:
            self._attr_preset_mode = PRESET_AUTO_MODE
            self._attr_percentage = ranged_value_to_percentage(SPEED_RANGE, fan_speed)
            # Only show as on if the fan is actually spinning
            self._attr_is_on = bool(fan_speed and fan_speed > 0)
        elif work_type == WORK_TYPE_ON:
            self._attr_is_on = True
            self._attr_preset_mode = PRESET_ON_MODE
            self._attr_percentage = ranged_value_to_percentage(SPEED_RANGE, fan_speed)
        else:
            self._attr_is_on = False
            self._attr_preset_mode = None
            self._attr_percentage = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attrs()
        super()._handle_coordinator_update()
