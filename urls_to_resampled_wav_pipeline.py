

from pathlib import Path

import concurrent_lines_download


def urls_to_resampled_wav_pipeline(
    source_txt: Path, out: Path, resampled_out: Path
) -> None:


    with source_txt.open() as f:
        lines = f.readlines()

    concurrent_lines_download.concurrent_lines_download(lines, out, resampled_out)