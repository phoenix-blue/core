"""Base Entity for Zeversolar sensors."""

from __future__ import annotations

from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ZeversolarCoordinator


class ZeversolarEntity(
    CoordinatorEntity[ZeversolarCoordinator],
):
    """Defines a base Zeversolar entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        *,
        coordinator: ZeversolarCoordinator,
    ) -> None:
        """Initialize the Zeversolar entity."""
        super().__init__(coordinator=coordinator)
        # Provide fallback device info when inverter is offline
        if coordinator.data:
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, coordinator.data.serial_number)},
                name="Zeversolar Sensor",
                manufacturer="Zeversolar",
                serial_number=coordinator.data.serial_number,
                suggested_area="Solar System",
            )
        else:
            # Use host-based identifier when offline
            host = coordinator.config_entry.data[CONF_HOST]
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, host)},
                name="Zeversolar Sensor",
                manufacturer="Zeversolar",
                suggested_area="Solar System",
            )
