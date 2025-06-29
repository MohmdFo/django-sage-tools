"""This module provides a comprehensive set of functions to convert between
different units of measurement.

It includes conversions between bytes and megabytes, days and seconds,
seconds and minutes, and various other common unit conversions.
"""

from typing import Union

from sage_tools.helpers.typings import Byte, Day, MegaByte, Minute, Second

Number = Union[int, float]


class UnitConvertor:
    """A utility class for converting units between various scales of measurement.

    This class provides static methods for converting between different units
    commonly used in software development and data processing.

    Examples:
        >>> # Convert file sizes
        >>> UnitConvertor.convert_byte_to_megabyte(1048576)  # 1 MB in bytes
        1.048576

        >>> # Convert time units
        >>> UnitConvertor.convert_days_to_seconds(1)  # 1 day
        86400
    """

    # Constants for accurate conversions
    BYTES_PER_KILOBYTE = 1024
    BYTES_PER_MEGABYTE = 1024**2  # 1,048,576 bytes
    BYTES_PER_GIGABYTE = 1024**3  # 1,073,741,824 bytes

    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400

    @staticmethod
    def convert_byte_to_megabyte(value: Byte) -> MegaByte:
        """Convert bytes to megabytes using binary conversion (1024^2).

        Args:
            value: The number of bytes.

        Returns:
            The equivalent number of megabytes.

        Examples:
            >>> UnitConvertor.convert_byte_to_megabyte(1048576)
            1.0
            >>> UnitConvertor.convert_byte_to_megabyte(2097152)
            2.0
        """
        if value < 0:
            raise ValueError("Byte value cannot be negative")
        return value / UnitConvertor.BYTES_PER_MEGABYTE

    @staticmethod
    def convert_megabyte_to_byte(value: MegaByte) -> Byte:
        """Convert megabytes to bytes using binary conversion (1024^2).

        Args:
            value: The number of megabytes.

        Returns:
            The equivalent number of bytes.

        Examples:
            >>> UnitConvertor.convert_megabyte_to_byte(1.0)
            1048576
            >>> UnitConvertor.convert_megabyte_to_byte(2.5)
            2621440
        """
        if value < 0:
            raise ValueError("Megabyte value cannot be negative")
        return int(value * UnitConvertor.BYTES_PER_MEGABYTE)

    @staticmethod
    def convert_byte_to_kilobyte(value: Byte) -> float:
        """Convert bytes to kilobytes.

        Args:
            value: The number of bytes.

        Returns:
            The equivalent number of kilobytes.
        """
        if value < 0:
            raise ValueError("Byte value cannot be negative")
        return value / UnitConvertor.BYTES_PER_KILOBYTE

    @staticmethod
    def convert_byte_to_gigabyte(value: Byte) -> float:
        """Convert bytes to gigabytes.

        Args:
            value: The number of bytes.

        Returns:
            The equivalent number of gigabytes.
        """
        if value < 0:
            raise ValueError("Byte value cannot be negative")
        return value / UnitConvertor.BYTES_PER_GIGABYTE

    @staticmethod
    def convert_days_to_seconds(value: Day) -> Second:
        """Convert days to seconds.

        Args:
            value: The number of days.

        Returns:
            The equivalent number of seconds.

        Examples:
            >>> UnitConvertor.convert_days_to_seconds(1)
            86400
            >>> UnitConvertor.convert_days_to_seconds(0.5)
            43200
        """
        if value < 0:
            raise ValueError("Day value cannot be negative")
        return int(value * UnitConvertor.SECONDS_PER_DAY)

    @staticmethod
    def convert_seconds_to_minutes(value: Second) -> Minute:
        """Convert seconds to minutes.

        Args:
            value: The number of seconds.

        Returns:
            The equivalent number of minutes.

        Examples:
            >>> UnitConvertor.convert_seconds_to_minutes(60)
            1.0
            >>> UnitConvertor.convert_seconds_to_minutes(90)
            1.5
        """
        if value < 0:
            raise ValueError("Second value cannot be negative")
        return value / UnitConvertor.SECONDS_PER_MINUTE

    @staticmethod
    def convert_minutes_to_seconds(value: Minute) -> Second:
        """Convert minutes to seconds.

        Args:
            value: The number of minutes.

        Returns:
            The equivalent number of seconds.

        Examples:
            >>> UnitConvertor.convert_minutes_to_seconds(1)
            60
            >>> UnitConvertor.convert_minutes_to_seconds(2.5)
            150
        """
        if value < 0:
            raise ValueError("Minute value cannot be negative")
        return int(value * UnitConvertor.SECONDS_PER_MINUTE)

    @staticmethod
    def convert_hours_to_seconds(value: Number) -> Second:
        """Convert hours to seconds.

        Args:
            value: The number of hours.

        Returns:
            The equivalent number of seconds.
        """
        if value < 0:
            raise ValueError("Hour value cannot be negative")
        return int(value * UnitConvertor.SECONDS_PER_HOUR)

    @staticmethod
    def convert_seconds_to_hours(value: Second) -> float:
        """Convert seconds to hours.

        Args:
            value: The number of seconds.

        Returns:
            The equivalent number of hours.
        """
        if value < 0:
            raise ValueError("Second value cannot be negative")
        return value / UnitConvertor.SECONDS_PER_HOUR

    @staticmethod
    def humanize_bytes(value: Byte, precision: int = 2) -> str:
        """Convert bytes to human-readable format.

        Args:
            value: The number of bytes.
            precision: Number of decimal places to show.

        Returns:
            Human-readable string representation.

        Examples:
            >>> UnitConvertor.humanize_bytes(1024)
            '1.00 KB'
            >>> UnitConvertor.humanize_bytes(1048576)
            '1.00 MB'
        """
        if value < 0:
            raise ValueError("Byte value cannot be negative")

        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = float(value)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.{precision}f} {units[unit_index]}"
