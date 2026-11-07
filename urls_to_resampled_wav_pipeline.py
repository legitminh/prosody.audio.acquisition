
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from download_segment import download_youtube_segment
from resample import resample

SEPARATORS = [
    "https://www.youtube.com/embed/",
    "?start=",
    "&end="
]

def separate_by_separators(line, sep):
    for i, v in enumerate(sep):
        index = line.find(v)
        yield line[:index]
        line = line[index+len(v):]
    yield line


def urls_to_resampled_wav_pipeline(
    source_txt: Path, out: Path, resampled_out: Path
) -> None:
    out.mkdir(parents=True, exist_ok=True)
    resampled_out.mkdir(parents=True, exist_ok=True)

    with source_txt.open() as f:
        lines = f.readlines()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i, line in enumerate(lines):
            _, code, start, end = separate_by_separators(line.strip(), SEPARATORS)
            print(f"Code: {code}, Start: {start}, End: {end}")
            futures.append(
                executor.submit(
                    download_youtube_segment,
                    video_url=f"https://www.youtube.com/watch?v={code}",
                    start_time=int(start),
                    end_time=int(end),
                    output=str(out / str(i)),
                )
            )

        for future in as_completed(futures):
            future.result()


    for i in out.glob("*.wav"):
        resample(i, resampled_out)