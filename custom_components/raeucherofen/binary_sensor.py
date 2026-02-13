"""Binary Sensor platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
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
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        RaeucherofenBinarySensor(coordinator, "running", "Betrieb", BinarySensorDeviceClass.RUNNING),
        RaeucherofenBinarySensor(coordinator, "heaterOn", "Heizung", BinarySensorDeviceClass.HEAT),
        RaeucherofenBinarySensor(coordinator, "dryFanEnabled", "Lüfter (Aktiv)", BinarySensorDeviceClass.FAN), # Logical state
        RaeucherofenBinarySensor(coordinator, "flapOpen", "Klappe (Offen)", BinarySensorDeviceClass.WINDOW),
        RaeucherofenBinarySensor(coordinator, "lightOn", "Licht", BinarySensorDeviceClass.LIGHT),
        RaeucherofenBinarySensor(coordinator, "smokePhaseOn", "Rauchphase", BinarySensorDeviceClass.RUNNING),
        RaeucherofenBinarySensor(coordinator, "waterPhaseOn", "Wasserphase", BinarySensorDeviceClass.RUNNING),
        RaeucherofenBinarySensor(coordinator, "cooldown", "Abkühlen Aktiv", BinarySensorDeviceClass.RUNNING),
        RaeucherofenBinarySensor(coordinator, "killSeq", "Notabschaltung Aktiv", BinarySensorDeviceClass.PROBLEM),
        RaeucherofenBinarySensor(coordinator, "powerCut", "Stromunterbrechung", BinarySensorDeviceClass.PROBLEM),
    ]
    
    async_add_entities(entities)

class RaeucherofenBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Binary Sensor."""

    def __init__(self, coordinator: RaeucherofenCoordinator, key: str, name: str, device_class: BinarySensorDeviceClass = None) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"
        self._attr_device_class = device_class

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get(self._key)
