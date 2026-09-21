"""Tests for video information formatting."""

from video_compressor.formatter import format_size
from video_compressor.formatter import format_duration
from video_compressor.formatter import format_bitrate


def test_format_size_bytes() -> None:
    """Format a small byte value."""
    assert format_size(500) == "500.0 B"


def test_format_size_kilobytes() -> None:
    """Format a kilobyte value."""
    assert format_size(1024) == "1.0 KB"


def test_format_size_megabytes() -> None:
    """Format a megabyte value."""
    assert format_size(47 * 1024 * 1024) == "47.0 MB"


def test_format_size_gigabytes() -> None:
    """Format a gigabyte value."""
    assert format_size(2 * 1024 * 1024 * 1024) == "2.0 GB"

def test_format_duration_seconds() -> None:
    """Format seconds into HH:MM:SS."""
    assert format_duration(45) == "00:00:45"


def test_format_duration_minutes() -> None:
    """Format minutes into HH:MM:SS."""
    assert format_duration(125) == "00:02:05"


def test_format_duration_hours() -> None:
    """Format hours into HH:MM:SS."""
    assert format_duration(3661) == "01:01:01"

def test_format_bitrate_kbps() -> None:
    """Format a bitrate below 1 Mbps."""
    assert format_bitrate(128_000) == "128 kbps"


def test_format_bitrate_mbps() -> None:
    """Format a bitrate in Mbps."""
    assert format_bitrate(1_250_000) == "1.25 Mbps"


def test_format_bitrate_none() -> None:
    """Handle a missing bitrate."""
    assert format_bitrate(None) == "Unknown"


