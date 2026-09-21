"""Tests for the command-line interface."""

from unittest.mock import patch

from click.testing import CliRunner

from video_compressor.cli import cli
from video_compressor.models import VideoInfo


@patch("video_compressor.cli.compress_video")
def test_compress_uses_explicit_output(mock_compress, tmp_path):
    """Test that compress uses an explicitly provided output path."""
    input_file = tmp_path / "video.mp4"
    output_file = tmp_path / "smaller.mp4"

    input_file.touch()

    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "compress",
            str(input_file),
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0

    mock_compress.assert_called_once_with(
        input_file=input_file,
        output_file=output_file,
        crf=23,
    )

@patch("video_compressor.cli.compress_video")
def test_compress_uses_default_output(mock_compress, tmp_path):
    """Test that compress uses the default output filename."""
    input_file = tmp_path / "video.mp4"
    input_file.touch()

    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["compress", str(input_file)],
    )

    assert result.exit_code == 0

    expected_output = tmp_path / "video_compressed_23.mp4"

    mock_compress.assert_called_once_with(
        input_file=input_file,
        output_file=expected_output,
        crf=23,
    )


@patch("video_compressor.cli.compress_video")
def test_compress_passes_custom_crf(mock_compress, tmp_path):
    """Test that compress passes a custom CRF value."""
    input_file = tmp_path / "video.mp4"
    input_file.touch()

    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "compress",
            str(input_file),
            "--crf",
            "28",
        ],
    )

    assert result.exit_code == 0

    expected_output = tmp_path / "video_compressed_28.mp4"

    mock_compress.assert_called_once_with(
        input_file=input_file,
        output_file=expected_output,
        crf=28,
    )


def test_compress_rejects_missing_input_file():
    """Test that compress rejects a nonexistent input file."""
    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["compress", "does_not_exist.mp4"],
    )

    assert result.exit_code != 0
    assert "does_not_exist.mp4" in result.output


@patch("video_compressor.cli.probe_video")
def test_info_calls_probe_video(mock_probe, tmp_path):
    """Test that info probes the requested video file."""
    input_file = tmp_path / "video.mp4"
    input_file.touch()

    mock_probe.return_value = VideoInfo(
        filename="video.mp4",
        size_bytes=1_000_000,
        duration_seconds=60.0,
        format_name="mov,mp4,m4a,3gp,3g2,mj2",
        bitrate=1_000_000,
        video_codec="h264",
        width=1920,
        height=1080,
        frame_rate=30.0,
        pixel_format="yuv420p",
        video_bitrate=900_000,
        audio_codec="aac",
        sample_rate=48_000,
        channels=2,
        audio_bitrate=128_000,
    )

    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["info", str(input_file)],
    )

    assert result.exit_code == 0

    mock_probe.assert_called_once_with(input_file)


@patch("video_compressor.cli.probe_video")
def test_info_displays_video_information(mock_probe, tmp_path):
    """Test that info displays the probed video information."""
    input_file = tmp_path / "video.mp4"
    input_file.touch()

    mock_probe.return_value = VideoInfo(
        filename="video.mp4",
        size_bytes=1 * 1024 * 1024,
        duration_seconds=60.0,
        format_name="mov,mp4,m4a,3gp,3g2,mj2",
        bitrate=1_000_000,
        video_codec="h264",
        width=1920,
        height=1080,
        frame_rate=30.0,
        pixel_format="yuv420p",
        video_bitrate=900_000,
        audio_codec="aac",
        sample_rate=48_000,
        channels=2,
        audio_bitrate=128_000,
    )

    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["info", str(input_file)],
    )

    assert result.exit_code == 0

    assert "Video Information" in result.output
    assert "video.mp4" in result.output
    assert "1.0 MB" in result.output
    assert "00:01:00" in result.output
    assert "MP4" in result.output
    assert "h264" in result.output
    assert "1920 × 1080" in result.output
    assert "30.00 fps" in result.output
    assert "aac" in result.output
    assert "Stereo" in result.output


@patch(
    "video_compressor.cli.compress_video",
    side_effect=FileNotFoundError("ffmpeg not found"),
)
def test_compress_shows_error_when_ffmpeg_is_missing(
    mock_compress,
    tmp_path,
) -> None:
    """Show a clean error when FFmpeg is not available."""
    input_file = tmp_path / "video.mp4"
    input_file.touch()

    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["compress", str(input_file)],
    )

    assert result.exit_code != 0
    assert "Error:" in result.output
    assert "FFmpeg" in result.output
    assert "not found" in result.output
