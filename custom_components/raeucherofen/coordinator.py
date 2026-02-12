"""DataUpdateCoordinator for Raeucherofen."""
from __future__ import annotations

import logging
from datetime import timedelta
import async_timeout
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_HOST, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class RaeucherofenCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self.host = entry.data[CONF_HOST]
        self.api_url = f"http://{self.host}/api"

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.api_url}/state") as response:
                        response.raise_for_status()
                        data = await response.json()
                        return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def async_send_command(self, endpoint: str, payload: dict = None):
        """Send a command to the API."""
        url = f"{self.api_url}/{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload) as response:
                    response.raise_for_status()
                    await self.async_request_refresh() # Force update after command
        except Exception as err:
            _LOGGER.error(f"Error sending command to {endpoint}: {err}")
