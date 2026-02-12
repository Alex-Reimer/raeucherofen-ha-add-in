"""Select platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROGRAM_MAPPING, REVERSE_PROGRAM_MAPPING
from .coordinator import RaeucherofenCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaeucherofenProgramSelect(coordinator)])
    async_add_entities([RaeucherofenSensorSelect(coordinator)])

class RaeucherofenProgramSelect(CoordinatorEntity, SelectEntity):
    _attr_name = "Program"
    _attr_options = list(PROGRAM_MAPPING.values())

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_program"

    @property
    def current_option(self) -> str | None:
        val = self.coordinator.data.get("program")
        return PROGRAM_MAPPING.get(val, "None")

    async def async_select_option(self, option: str) -> None:
        val = REVERSE_PROGRAM_MAPPING.get(option)
        if val is not None:
             await self.coordinator.async_send_command("program", {"p": val})

class RaeucherofenSensorSelect(CoordinatorEntity, SelectEntity):
    _attr_name = "Control Sensor"
    _attr_options = ["oben", "mitte", "unten"]

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_active_sensor"

    @property
    def current_option(self) -> str | None:
        return self.coordinator.data.get("sensor")

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_send_command("sensor", {"s": option})
