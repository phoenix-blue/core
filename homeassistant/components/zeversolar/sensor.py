"""Support for the Zeversolar platform."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import zeversolar

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EntityCategory, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import ZeversolarCoordinator
from .entity import ZeversolarEntity


@dataclass(frozen=True, kw_only=True)
class ZeversolarEntityDescription(SensorEntityDescription):
    """Describes Zeversolar sensor entity."""

    value_fn: Callable[
        [zeversolar.ZeverSolarData | None], zeversolar.kWh | zeversolar.Watt | str
    ]


SENSOR_TYPES = (
    ZeversolarEntityDescription(
        key="pac",
        translation_key="pac",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.POWER,
        value_fn=lambda data: data.pac if data else 0,
    ),
    ZeversolarEntityDescription(
        key="energy_today",
        translation_key="energy_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        value_fn=lambda data: data.energy_today if data else 0,
    ),
    ZeversolarEntityDescription(
        key="status",
        translation_key="status",
        device_class=SensorDeviceClass.ENUM,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: "online" if data else "offline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Zeversolar sensor."""
    coordinator: ZeversolarCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ZeversolarSensor(
            description=description,
            coordinator=coordinator,
        )
        for description in SENSOR_TYPES
    )


class ZeversolarSensor(ZeversolarEntity, SensorEntity):
    """Implementation of the Zeversolar sensor."""

    entity_description: ZeversolarEntityDescription

    def __init__(
        self,
        *,
        description: ZeversolarEntityDescription,
        coordinator: ZeversolarCoordinator,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(coordinator=coordinator)
        # Use host-based identifier as fallback when offline
        if coordinator.data:
            self._attr_unique_id = (
                f"{coordinator.data.serial_number}_{description.key}"
            )
        else:
            host = coordinator.config_entry.data[CONF_HOST]
            self._attr_unique_id = f"{host}_{description.key}"
        # Track last known value for energy sensor
        self._last_known_value: int | float | str | None = None

    @property
    def native_value(self) -> int | float | str:
        """Return sensor state."""
        value = self.entity_description.value_fn(self.coordinator.data)
        # Preserve last known energy value when offline
        if self.entity_description.key == "energy_today" and value == 0:
            if self._last_known_value is not None and self._last_known_value > 0:
                return self._last_known_value
        # Update last known value when online
        if value != 0 or self.entity_description.key == "status":
            self._last_known_value = value
        return value

    @property
    def available(self) -> bool:
        """Return True to prevent 'unavailable' state during offline periods."""
        return True
