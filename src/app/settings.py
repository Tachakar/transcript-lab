import logging
import subprocess
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_root_path():
    root = Path(__file__)
    MARKERS = ['requirements.txt', 'pyproject.toml', '.git', 'README.md']

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

    @staticmethod
    def check_or_create_path(path:Path):
        if path.exists():
            return
        path.mkdir(parents=True, exist_ok=True)
        return

    youtube_api_key: str

    PROJECT_ROOT_PATH: Path = get_root_path()
    DATA_DIR_PATH: Path = PROJECT_ROOT_PATH/"data"

settings = Settings()
