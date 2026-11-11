
from pathlib import Path

from url_sourcing import search_filmot
import concurrent_lines_download

def query_to_resampled_wav_pipeline(query: str, out: Path, out_txt: Path | None, resampled_out: Path, num_videos: int = 10):
    dict_line = search_filmot(query, n=num_videos)
    lines = list(i["url"] for i in dict_line["videos"])
    if out_txt is not None:
        with out_txt.open("w") as f:
            for line in lines:
                f.write(line + "\n")
    concurrent_lines_download.concurrent_lines_download(lines, out, resampled_out)


