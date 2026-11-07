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
    start_time = time()
    title = "somepeople"
    urls_to_resampled_wav_pipeline(
        DIR_URLS / f"{title}.txt",
        DIR_WAV / title,
        DIR_RESAMPLED / title
    )
    end_time = time()
    print(f"Total processing time: {end_time - start_time} seconds")