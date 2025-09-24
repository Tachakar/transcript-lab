import logging
import subprocess
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
MARKERS = ['requirements.txt', 'pyproject.toml', '.git', 'README.md']

def get_root_path():
    root = Path(__file__)

    try:
        x = subprocess.run(["git", "rev-parse", "--show-toplevel"],capture_output=True,text=True,check=True)
        root = Path(x.stdout.strip())

    except subprocess.CalledProcessError:
        start = root.resolve()
        found = False
        for ancestor in [start] + list(start.parents):
            for marker in MARKERS:
                if (ancestor/marker).exists():
                    root = ancestor
                    found = True
                    break
            if found:
                break
    except Exception as e:
        logging.warning(f"Can't find project root path. Setting root as settings.py directory. Error: {e}")
        root = root.parent

    return root

class Settings(BaseSettings):

    # Keys
    youtube_api_key: str

    # Paths
    PROJECT_ROOT_PATH: Path = get_root_path()
    DATA_DIR_PATH: Path = PROJECT_ROOT_PATH/"data"
    AUDIO_DIR_PATH: Path =DATA_DIR_PATH/"audio"
    TRANSCRIPTS_DIR_PATH: Path = DATA_DIR_PATH/"transcripts"
    RAW_TRANSCRIPTS_DIR_PATH: Path = TRANSCRIPTS_DIR_PATH/"raw"
    CLEAN_TRANSCRIPTS_DIR_PATH: Path = TRANSCRIPTS_DIR_PATH/"clean"


def prepare_dirs(settings: Settings):
    try:
        for _, value in settings:
            if isinstance(value,Path):
                path = Path(value)
                path.mkdir(parents=True, exist_ok = True)
    except Exception as e:
        logging.warning(f"Something went wrong. LOG: {e}")
