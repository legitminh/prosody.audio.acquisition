from pathlib import Path
import subprocess


def resample(file_path: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "sox",
            str(file_path),
            str(out / file_path.name),
            "channels",
            "1",
            "rate",
            "-v",
            "16k",
            "gain",
            "-3",
        ],
        check=True,
    )

if __name__ == "__main__":
    for i in Path("wav", "muchasidid.txt").glob("*.wav"):
        resample(i, Path("16KHz/wav"))