import subprocess
import yt_dlp.utils
import yt_dlp
from typing import Any
from pathlib import Path

DIR_URLS = Path("urls")

#lines 
SEPARATORS = [
    "https://www.youtube.com/embed/",
    "?start=",
    "&end="
]

DIR_WAV = Path("wav")
DIR_WAV.mkdir(parents=True, exist_ok=True)

def download_youtube_segment(video_url, start_time, end_time, output_name="segment"):
    """
    Downloads a specific segment of a YouTube video.
    
    :param video_url: Full URL of the YouTube video.
    :param start_time: Start time of the segment in seconds (int/float) or "HH:MM:SS" format.
    :param end_time: End time of the segment in seconds (int/float) or "HH:MM:SS" format.
    :param output_name: The name of the output file (excluding extension).
    """
    
    # Configure yt-dlp options to download only the requested segment
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'wav',
        'outtmpl': f'{output_name}.%(ext)s',
        # download_ranges expects a list of dicts with start_time and end_time
        'download_ranges': lambda info, ctx: [{
            'start_time': start_time,
            'end_time': end_time,
            'title': info.get('title', 'segment')
        }],
        # Required parameter for download_ranges to work seamlessly
        'force_keyframes_at_cuts': True, 
    }

    try:
        print(f"Initializing download for segment: {start_time} to {end_time}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore[arg-type]
            ydl.download([video_url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def separate_by_separators(line, sep):
    for i, v in enumerate(sep):
        index = line.find(v)
        yield line[:index]
        line = line[index+len(v):]
    yield line

DUR_URL_MUCHASIDID = DIR_URLS / "muchasidid.txt"
DUR_WAV_MUCHASIDID = DIR_WAV / "muchasidid.txt"
with DUR_URL_MUCHASIDID.open() as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        _, code, start, end = separate_by_separators(line, SEPARATORS)

        outtmpl = str(DIR_WAV / f"{i}.wav")
        print(f"Code: {code}, Start: {start}, End: {end}")

        # download_youtube_segment(
        #     video_url=f"https://www.youtube.com/watch?v={code}",
        #     start_time=int(start),
        #     end_time=int(end),
        #     output_name=str(DIR_WAV / f"{i}")
        # )

        """
        yt-dlp -x --audio-format wav --download-sections "*150-160" -o "my_audio_clip.%(ext)s" "https://www.youtube.com/watch?v=yLhX3goJgPs"
        """
        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format",
                "wav",
                "--download-sections",
                f"*{start}-{end}",
                "-o",
                str(DUR_WAV_MUCHASIDID / f"{i}.%(ext)s"),
                f"https://www.youtube.com/watch?v={code}",
            ],
            # check=True,
        )
