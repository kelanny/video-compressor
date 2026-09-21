"""Video inspection functionality."""

from fractions import Fraction
import json
import subprocess
from pathlib import Path

from video_compressor.models import VideoInfo


def parse_frame_rate(value: str | None) -> float | None:
    """Convert an FFmpeg frame-rate fraction to a float."""
    if not value or value == "0/0":
        return None

    return float(Fraction(value))

def probe_video(input_file: Path) -> VideoInfo:
    """Return information about a video using FFprobe."""
    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(input_file),
    ]

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)

    format_data = data["format"]

    video_stream = next(
        (
            stream
            for stream in data["streams"]
            if stream["codec_type"] == "video"
        ),
        None,
    )

    audio_stream = next(
        (
            stream
            for stream in data["streams"]
            if stream["codec_type"] == "audio"
        ),
        None,
    )

    return VideoInfo(
        filename=input_file.name,
        size_bytes=int(format_data["size"]),
        duration_seconds=float(format_data["duration"]),
        format_name=format_data["format_name"],
        bitrate=int(format_data["bit_rate"]),
        video_codec=video_stream["codec_name"] if video_stream else None,
        width=video_stream["width"] if video_stream else None,
        height=video_stream["height"] if video_stream else None,
        frame_rate=(
            parse_frame_rate(video_stream.get("avg_frame_rate"))
            if video_stream
            else None
),
        pixel_format=(
            video_stream["pix_fmt"]
            if video_stream
            else None
        ),
        video_bitrate=(
            int(video_stream["bit_rate"])
            if video_stream and video_stream.get("bit_rate")
            else None
        ),
        audio_codec=(
            audio_stream["codec_name"]
            if audio_stream
            else None
        ),
        sample_rate=(
            int(audio_stream["sample_rate"])
            if audio_stream and audio_stream.get("sample_rate")
            else None
        ),
        channels=(
            audio_stream["channels"]
            if audio_stream
            else None
        ),
        audio_bitrate=(
            int(audio_stream["bit_rate"])
            if audio_stream and audio_stream.get("bit_rate")
            else None
        ),
    )
