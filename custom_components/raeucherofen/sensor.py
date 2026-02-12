"""Sensor platform for Raeucherofen."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
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
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        RaeucherofenTempSensor(coordinator, "t_top", "Top Temperature"),
        RaeucherofenTempSensor(coordinator, "t_mid", "Middle Temperature"),
        RaeucherofenTempSensor(coordinator, "t_bot", "Bottom Temperature"),
        RaeucherofenTempSensor(coordinator, "t_meat", "Meat Temperature"),
        RaeucherofenTempSensor(coordinator, "t_out", "Outside Temperature"),
        RaeucherofenTimeSensor(coordinator, "remaining_s", "Time Remaining"),
        RaeucherofenTimeSensor(coordinator, "smokePhaseRemaining_s", "Smoke Phase Remaining"),
        RaeucherofenTimeSensor(coordinator, "waterPhaseRemaining_s", "Water Phase Remaining"),
        RaeucherofenTextSensor(coordinator, "alarm", "Status Message"),
        RaeucherofenTextSensor(coordinator, "sensor", "Active Sensor"),
    ]
    
    async_add_entities(entities)

class RaeucherofenTempSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Temperature Sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: RaeucherofenCoordinator, key: str, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        val = self.coordinator.data.get(self._key)
        if val == "--.-":
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

class RaeucherofenTimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Time Sensor."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS

    def __init__(self, coordinator: RaeucherofenCoordinator, key: str, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)

class RaeucherofenTextSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Text Sensor."""

    def __init__(self, coordinator: RaeucherofenCoordinator, key: str, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)
