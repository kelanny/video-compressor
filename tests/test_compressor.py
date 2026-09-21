"""Tests for video compression functionality."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from video_compressor.compressor import compress_video


@patch("video_compressor.compressor.subprocess.run")
def test_compress_video_builds_ffmpeg_command(mock_run, tmp_path):
    """Test that compress_video builds the expected FFmpeg command."""
    input_file = tmp_path / "input.mp4"
    output_file = tmp_path / "output.mp4"

    compress_video(
        input_file=input_file,
        output_file=output_file,
        crf=26,
    )

    expected_command = [
        "ffmpeg",
        "-i",
        str(input_file),
        "-c:v",
        "libx264",
        "-crf",
        "26",
        "-preset",
        "medium",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        str(output_file),
    ]

    mock_run.assert_called_once_with(
        expected_command,
        check=True,
    )



@patch("video_compressor.compressor.subprocess.run")
def test_compress_video_propagates_ffmpeg_failure(mock_run, tmp_path):
    """Test that an FFmpeg failure is propagated to the caller."""
    input_file = tmp_path / "input.mp4"
    output_file = tmp_path / "output.mp4"

    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["ffmpeg"],
    )

    with pytest.raises(subprocess.CalledProcessError):
        compress_video(
            input_file=input_file,
            output_file=output_file,
            crf=26,
        )


def test_compress_video_raises_when_ffmpeg_is_missing() -> None:
    """Raise FileNotFoundError when FFmpeg is not installed."""
    with patch(
        "video_compressor.compressor.subprocess.run",
        side_effect=FileNotFoundError("ffmpeg not found"),
    ):
        with pytest.raises(FileNotFoundError):
            compress_video(
                input_file=Path("input.mp4"),
                output_file=Path("output.mp4"),
            )



