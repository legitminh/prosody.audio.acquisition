
def download_youtube_segment_library(video_url, start_time, end_time, output):
    import yt_dlp.utils
    import yt_dlp
    """
    Downloads a specific segment of a YouTube video.
    
    :param video_url: Full URL of the YouTube video.
    :param start_time: Start time of the segment in seconds (int/float) or "HH:MM:SS" format.
    :param end_time: End time of the segment in seconds (int/float) or "HH:MM:SS" format.
    :param output: The path to the output file (excluding extension).
    """
    
    # Configure yt-dlp options to download only the requested segment
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'wav',
        'outtmpl': f'{output}.%(ext)s',
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

def download_youtube_segment_cli(video_url, start_time, end_time, output):
    """
    yt-dlp -x --audio-format wav --download-sections "*150-160" -o "my_audio_clip.%(ext)s" "https://www.youtube.com/watch?v=yLhX3goJgPs"
    """
    import subprocess
    from pathlib import Path

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format",
            "wav",
            "--download-sections",
            f"*{start_time}-{end_time}",
            "-o",
            str(f"{output}.%(ext)s"),
            video_url,
        ],
        check=True,
    )


def download_youtube_segment(video_url, start_time, end_time, output):
    download_youtube_segment_cli(video_url, start_time, end_time, output)