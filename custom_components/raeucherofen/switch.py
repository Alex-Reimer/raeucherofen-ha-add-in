"""Switch platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        RaeucherofenSwitch(coordinator, "dryFanEnabled", "Dry Fan Override", "dryfan", "en"),
        RaeucherofenSwitch(coordinator, "flapOpen", "Flap Override", "flap", "open"),
        RaeucherofenSwitch(coordinator, "lightOn", "Light", "light", "en"),
        RaeucherofenMeatEnableSwitch(coordinator),
        RaeucherofenSmokeContinuousSwitch(coordinator),
    ]
    
    async_add_entities(entities)

class RaeucherofenSwitch(CoordinatorEntity, SwitchEntity):
    """Generic switch."""

    def __init__(self, coordinator: RaeucherofenCoordinator, key: str, name: str, api_cmd: str, api_param: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._api_cmd = api_cmd
        self._api_param = api_param
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}_switch"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get(self._key)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_send_command(self._api_cmd, {self._api_param: 1})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_send_command(self._api_cmd, {self._api_param: 0})

class RaeucherofenMeatEnableSwitch(CoordinatorEntity, SwitchEntity):
    _attr_name = "Meat Sensor Control Enabled"

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_meatEndEnabled"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get("meatEndEnabled")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_send_command("meat", {"en": 1})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_send_command("meat", {"en": 0})

class RaeucherofenSmokeContinuousSwitch(CoordinatorEntity, SwitchEntity):
    _attr_name = "Smoke Continuous"

    def __init__(self, coordinator: RaeucherofenCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_smokeContinuous"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get("smokeContinuous")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_send_command("smoke", {"continuous": 1})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_send_command("smoke", {"continuous": 0})
