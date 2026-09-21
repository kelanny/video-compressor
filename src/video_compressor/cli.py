"""Command-line interface for video compressor."""

from pathlib import Path

import click

from video_compressor.compressor import compress_video
from video_compressor.probe import probe_video
from video_compressor.formatter import format_video_info


@click.group()
def cli() -> None:
    """Compress and inspect video files."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    help="Output video path.",
)
@click.option(
        "--crf",
        default=23,
        show_default=True,
        type=click.IntRange(1,50),
        help="Constant rate factor. Lower values produce high quality and Larger value.",
        )
def compress(input_file: Path, output: Path | None, crf: int) -> None:
    """Compress a video file."""
    if output is None:
        output = input_file.with_stem(
                f"{input_file.stem}_compressed_{crf}"
                )

    compress_video(
        input_file=input_file,
        output_file=output,
        crf=crf,
    )

    click.echo(f"Compressed video: {output}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
def info(input_file: Path) -> None:
    """Display information about a video."""
    video_info = probe_video(input_file)

    click.echo()
    click.echo("*" * 40)
    click.echo(format_video_info(video_info))
    click.echo("*" * 40)
    click.echo()
