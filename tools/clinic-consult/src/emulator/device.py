"""uiautomator2 device connection manager.

Handles connecting to an Android device/emulator via uiautomator2 with
automatic retry logic and graceful reconnection.
"""

from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)

try:
    import uiautomator2 as u2
except ImportError:
    u2 = None  # type: ignore[assignment]
    logger.warning(
        "uiautomator2 is not installed. Install it with: pip install uiautomator2"
    )


class DeviceManager:
    """Manage a uiautomator2 device connection with retry logic.

    Parameters
    ----------
    serial:
        ADB serial address of the device (e.g. ``127.0.0.1:5555``).
    max_retries:
        Maximum number of connection attempts before giving up.
    """

    def __init__(
        self, serial: str = "127.0.0.1:5555", max_retries: int = 5
    ) -> None:
        self.serial = serial
        self.max_retries = max_retries
        self._device: u2.Device | None = None  # type: ignore[name-defined]

    def connect(self) -> u2.Device:  # type: ignore[name-defined]
        """Connect to the device with retry logic.

        Returns
        -------
        u2.Device
            A connected uiautomator2 device instance.

        Raises
        ------
        RuntimeError
            If uiautomator2 is not installed.
        ConnectionError
            If all connection attempts fail.
        """
        if u2 is None:
            raise RuntimeError(
                "uiautomator2 is not installed. "
                "Install it with: pip install uiautomator2"
            )

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    "Connecting to device %s (attempt %d/%d)",
                    self.serial,
                    attempt,
                    self.max_retries,
                )
                device = u2.connect(self.serial)
                # Verify the connection is alive
                device.info  # noqa: B018 -- intentional attribute access
                self._device = device
                logger.info("Connected to device %s", self.serial)
                return device
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Connection attempt %d/%d failed: %s",
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 30))  # exponential backoff, max 30s

        raise ConnectionError(
            f"Failed to connect to device {self.serial} "
            f"after {self.max_retries} attempts: {last_error}"
        )

    def ensure_connected(self) -> u2.Device:  # type: ignore[name-defined]
        """Return the current device or reconnect if necessary.

        Returns
        -------
        u2.Device
            A connected uiautomator2 device instance.
        """
        if self._device is not None:
            try:
                self._device.info  # noqa: B018 -- connectivity check
                return self._device
            except Exception:
                logger.info("Device connection lost, reconnecting...")
                self._device = None

        return self.connect()

    def disconnect(self) -> None:
        """Disconnect from the device and clear internal state."""
        if self._device is not None:
            logger.info("Disconnecting from device %s", self.serial)
            self._device = None

    @property
    def is_connected(self) -> bool:
        """Return ``True`` if a device connection is currently active."""
        if self._device is None:
            return False
        try:
            self._device.info  # noqa: B018 -- connectivity check
            return True
        except Exception:
            self._device = None
            return False
