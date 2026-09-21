"""Data models for video information."""

from dataclasses import dataclass


@dataclass
class VideoInfo:
    """Information about a video file."""

    filename: str
    size_bytes: int
    duration_seconds: float
    format_name: str
    bitrate: int | None

    video_codec: str | None
    width: int | None
    height: int | None
    frame_rate: float | None
    pixel_format: str | None
    video_bitrate: int | None

    audio_codec: str | None
    sample_rate: int | None
    channels: int | None
    audio_bitrate: int | None
