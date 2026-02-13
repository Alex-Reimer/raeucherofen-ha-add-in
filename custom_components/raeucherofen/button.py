"""Button platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([
        RaeucherofenButton(coordinator, "Programm Starten", "running", {"r": 1}),
        RaeucherofenButton(coordinator, "Programm Stoppen", "running", {"r": 0}),
        RaeucherofenButton(coordinator, "Komplett Ausschalten", "poweroff", {}),
    ])

class RaeucherofenButton(CoordinatorEntity, ButtonEntity):
    """Representation of a Button."""

    def __init__(self, coordinator: RaeucherofenCoordinator, name: str, api_cmd: str, payload: dict) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._api_cmd = api_cmd
        self._payload = payload
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{api_cmd}_{name}"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_send_command(self._api_cmd, self._payload)
