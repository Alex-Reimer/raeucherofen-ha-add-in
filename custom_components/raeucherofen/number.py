"""Number platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RaeucherofenCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        RaeucherofenSetTemp(coordinator),
        RaeucherofenMeatTarget(coordinator),
        RaeucherofenDuration(coordinator),
        RaeucherofenSmokeOn(coordinator),
        RaeucherofenSmokeOff(coordinator),
        RaeucherofenSteamOn(coordinator),
        RaeucherofenSteamOff(coordinator),
    ]
    
    async_add_entities(entities)

class RaeucherofenSetTemp(CoordinatorEntity, NumberEntity):
    _attr_name = "Target Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0
    _attr_native_max_value = 120
    _attr_native_step = 0.5

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_setTemp"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("setTemp")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("settemp", {"v": value})

class RaeucherofenMeatTarget(CoordinatorEntity, NumberEntity):
    _attr_name = "Meat Target Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_meatTarget"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("meatTarget")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("meat", {"t": value})

class RaeucherofenDuration(CoordinatorEntity, NumberEntity):
    _attr_name = "Duration (Minutes)"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 1
    _attr_native_max_value = 1440
    _attr_native_step = 1

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_duration"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("duration_s", 0) / 60

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("duration", {"min": int(value)})

class RaeucherofenSmokeOn(CoordinatorEntity, NumberEntity):
    _attr_name = "Smoke On Duration"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_native_min_value = 1
    _attr_native_max_value = 600

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_smokeOn"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("smokeOnMin")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("smoke", {"on": int(value)})

class RaeucherofenSmokeOff(CoordinatorEntity, NumberEntity):
    _attr_name = "Smoke Off Duration"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_native_min_value = 1
    _attr_native_max_value = 600

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_smokeOff"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("smokeOffMin")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("smoke", {"off": int(value)})

class RaeucherofenSteamOn(CoordinatorEntity, NumberEntity):
    _attr_name = "Steam On Duration"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_native_min_value = 1
    _attr_native_max_value = 600

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_waterOn"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("waterOnSec")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("steam", {"on_s": int(value)})

class RaeucherofenSteamOff(CoordinatorEntity, NumberEntity):
    _attr_name = "Steam Off Duration"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_native_min_value = 1
    _attr_native_max_value = 1440

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_waterOff"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("waterOffMin")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command("steam", {"off_min": int(value)})
