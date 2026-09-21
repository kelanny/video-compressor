"""Video compression functionality."""

from pathlib import Path
import subprocess


def compress_video(
    input_file: Path,
    output_file: Path,
) -> None:
    """Compress a video using FFmpeg."""
    command = [
        "ffmpeg",
        "-i",
        str(input_file),
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-preset",
        "medium",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        str(output_file),
    ]

    subprocess.run(command, check=True)
