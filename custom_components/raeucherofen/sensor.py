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
        RaeucherofenTimeSensor(coordinator, "killLeft_s", "Kill Sequence Timer"),
        RaeucherofenTextSensor(coordinator, "alarm", "Status Message"),
        RaeucherofenTextSensor(coordinator, "sensor", "Active Sensor"),
        RaeucherofenStepSensor(coordinator, "krakauerStep", "Krakauer Step"),
        RaeucherofenStepSensor(coordinator, "indStep", "Individual Step"),
        RaeucherofenStepSensor(coordinator, "indTotal", "Individual Total Steps"),
        RaeucherofenTempSensor(coordinator, "maxTemp", "Max Allowed Temperature"),
    ]
    
    async_add_entities(entities)

class RaeucherofenStepSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Step Counter Sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

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



def format_duration(seconds):
    """Format seconds into a human readable string."""
    if seconds is None:
        return None
    try:
        seconds = int(float(seconds))
    except (ValueError, TypeError):
        return None

    if seconds < 60:
        return f"{seconds} Sek"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    if minutes < 60:
        if remaining_seconds > 0:
            return f"{minutes} Min {remaining_seconds} Sek"
        return f"{minutes} Min"
        
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes > 0:
        return f"{hours} Std {remaining_minutes} Min"
    return f"{hours} Std"

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
            return round(float(val), 1)
        except (ValueError, TypeError):
            return None

class RaeucherofenTimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Time Sensor."""

    # Time sensors now return a string, so no device class or unit of measurement
    _attr_icon = "mdi:timer"

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
        return format_duration(val)


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
