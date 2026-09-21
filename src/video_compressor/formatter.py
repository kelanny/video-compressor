"""Formatting utilities for video information."""

from video_compressor.models import VideoInfo


def format_size(size_bytes: int) -> str:
    """Format a byte value as a human-readable file size."""
    size = float(size_bytes)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    total_seconds = int(seconds)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_bitrate(bitrate: int | None) -> str:
    """Format a bitrate as a human-readable value."""
    if bitrate is None:
        return "Unknown"

    if bitrate < 1_000_000:
        return f"{bitrate / 1_000:.0f} kbps"

    return f"{bitrate / 1_000_000:.2f} Mbps"


def format_format_name(format_name: str) -> str:
    """Return a human-friendly container format name."""
    formats = format_name.split(",")

    if "mp4" in formats:
        return "MP4"

    if formats:
        return formats[0].upper()

    return "Unknown"


def format_frame_rate(frame_rate: float | None) -> str:
    """Format a frame rate."""
    if frame_rate is None:
        return "Unknown"

    return f"{frame_rate:.2f} fps"


def format_channels(channels: int | None) -> str:
    """Format an audio channel count."""
    if channels is None:
        return "None"

    channel_names = {
        1: "Mono",
        2: "Stereo",
    }

    return channel_names.get(channels, f"{channels} channels")


def format_video_info(video_info: VideoInfo) -> str:
    """Format video information for terminal display."""
    lines = [
        "Video Information",
        "────────────────────────────────────",
        f"File          {video_info.filename}",
        f"Size          {format_size(video_info.size_bytes)}",
        f"Duration      {format_duration(video_info.duration_seconds)}",
        f"Format        {format_format_name(video_info.format_name)}",
        f"Overall       {format_bitrate(video_info.bitrate)}",
        "",
        "Video",
        "────────────────────────────────────",
        f"Codec         {video_info.video_codec or 'Unknown'}",
        (
            f"Resolution    "
            f"{video_info.width} × {video_info.height}"
            if video_info.width and video_info.height
            else "Resolution    Unknown"
        ),
        f"Frame rate    {format_frame_rate(video_info.frame_rate)}",
        f"Pixel format  {video_info.pixel_format or 'Unknown'}",
        f"Bitrate       {format_bitrate(video_info.video_bitrate)}",
        "",
        "Audio",
        "────────────────────────────────────",
        f"Codec         {video_info.audio_codec or 'None'}",
        f"Sample rate   {video_info.sample_rate or 'Unknown'} Hz",
        f"Channels      {format_channels(video_info.channels)}",
        f"Bitrate       {format_bitrate(video_info.audio_bitrate)}",
    ]

    return "\n".join(lines)
