from time import time
from pathlib import Path
from urls_to_resampled_wav_pipeline import urls_to_resampled_wav_pipeline

#source file
DIR_URLS = Path("urls")

DIR_WAV = Path("wav")
DIR_WAV.mkdir(parents=True, exist_ok=True)

DIR_RESAMPLED = Path("16KHz/wav")
DIR_RESAMPLED.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    start_time: float = time()
    title = "object"
    # urls_to_resampled_wav_pipeline(
    #     DIR_URLS / f"{title}.txt",
    #     DIR_WAV / title,
    #     DIR_RESAMPLED / title
    # )
    from query_to_resampled_wav_pipeline import query_to_resampled_wav_pipeline
    query_to_resampled_wav_pipeline(
        query="object",
        out=DIR_WAV / title,
        out_txt=DIR_URLS / f"{title}.txt",
        resampled_out=DIR_RESAMPLED / title,
        num_videos=1
    )
    end_time: float = time()
    print(f"Total processing time: {end_time - start_time} seconds")