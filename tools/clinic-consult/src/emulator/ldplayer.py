"""LDPlayer lifecycle management via ldconsole subprocess calls.

Provides start/stop/query operations against an LDPlayer Android emulator
instance, plus the ability to run arbitrary ADB commands and launch apps.
"""

from __future__ import annotations

import logging
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class LDPlayerManager:
    """Manage a single LDPlayer emulator instance.

    Parameters
    ----------
    ldplayer_path:
        Root directory of the LDPlayer installation
        (e.g. ``C:/LDPlayer/LDPlayer9``).
    instance_name:
        Display name of the emulator instance to control.
    """

    def __init__(self, ldplayer_path: str, instance_name: str) -> None:
        self._ldplayer_path = Path(ldplayer_path)
        self.instance_name = instance_name

    @property
    def _ldconsole_path(self) -> Path:
        """Full path to the ``ldconsole.exe`` binary."""
        return self._ldplayer_path / "ldconsole.exe"

    def _run_command(self, args: list[str]) -> str:
        """Execute an ldconsole command and return its stdout.

        Parameters
        ----------
        args:
            Arguments to pass to ldconsole (e.g. ``["launch", "--name", "LDPlayer"]``).

        Returns
        -------
        str
            Captured standard output from the process.

        Raises
        ------
        subprocess.CalledProcessError
            If the command exits with a non-zero return code.
        subprocess.TimeoutExpired
            If the command does not complete within 30 seconds.
        FileNotFoundError
            If the ldconsole binary does not exist at the expected path.
        """
        cmd = [str(self._ldconsole_path), *args]
        logger.debug("Running ldconsole command: %s", cmd)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        result.check_returncode()
        return result.stdout.strip()

    def start(self) -> bool:
        """Launch the emulator instance and wait up to 30 s for it to run.

        Returns
        -------
        bool
            ``True`` if the instance is running after the wait period.
        """
        try:
            self._run_command(["launch", "--name", self.instance_name])
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.exception("Failed to launch LDPlayer instance %s", self.instance_name)
            return False

        # Poll until the instance reports as running (max ~30 s).
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if self.is_running():
                logger.info("LDPlayer instance %s is running", self.instance_name)
                return True
            time.sleep(1)

        logger.warning(
            "LDPlayer instance %s did not start within 30 s", self.instance_name
        )
        return False

    def stop(self) -> bool:
        """Gracefully stop the emulator instance.

        Returns
        -------
        bool
            ``True`` if the quit command succeeded.
        """
        try:
            self._run_command(["quit", "--name", self.instance_name])
            logger.info("LDPlayer instance %s stopped", self.instance_name)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.exception("Failed to stop LDPlayer instance %s", self.instance_name)
            return False

    def is_running(self) -> bool:
        """Check whether the emulator instance is currently running.

        Parses the output of ``ldconsole list2`` to find the instance
        and inspect its status column.
        """
        try:
            output = self._run_command(["list2"])
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

        for line in output.splitlines():
            if self.instance_name in line and "running" in line.lower():
                return True
        return False

    def launch_app(self, package_name: str) -> bool:
        """Launch an Android application inside the emulator.

        Parameters
        ----------
        package_name:
            Fully-qualified package name (e.g. ``com.kakao.talk``).

        Returns
        -------
        bool
            ``True`` if the ADB start command succeeded.
        """
        try:
            self.adb_command(
                f"shell am start -n {package_name}/.main.MainActivity"
            )
            logger.info("Launched app %s on %s", package_name, self.instance_name)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.exception("Failed to launch app %s", package_name)
            return False

    def adb_command(self, command: str) -> str:
        """Run an arbitrary ADB command inside the emulator.

        Parameters
        ----------
        command:
            ADB command string (e.g. ``"shell pm list packages"``).

        Returns
        -------
        str
            Standard output from the ADB command.
        """
        return self._run_command(
            ["adb", "--name", self.instance_name, "--command", command]
        )
