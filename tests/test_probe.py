"""Tests for video probing."""

from video_compressor.probe import parse_frame_rate


def test_parse_frame_rate_integer() -> None:
    """Parse an integer frame-rate fraction."""
    assert parse_frame_rate("30/1") == 30.0


def test_parse_frame_rate_ntsc() -> None:
    """Parse a fractional NTSC frame rate."""
    assert parse_frame_rate("30000/1001") == 29.97002997002997


def test_parse_frame_rate_zero() -> None:
    """Handle an undefined frame rate."""
    assert parse_frame_rate("0/0") is None


def test_parse_frame_rate_none() -> None:
    """Handle a missing frame rate."""
    assert parse_frame_rate(None) is None
