"""Command-line interface for video compressor."""

from pathlib import Path

import click

from video_compressor.compressor import compress_video


@click.group()
def cli() -> None:
    """Compress and inspect video files."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
def compress(input_file: Path) -> None:
    """Compress a video file."""
    output_file = input_file.with_stem(
        f"{input_file.stem}_compressed"
    )

    compress_video(
        input_file=input_file,
        output_file=output_file,
    )

    click.echo(f"Compressed video: {output_file}")
