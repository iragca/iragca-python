from enum import Enum
from pathlib import Path

STYLES_DIR = Path(__file__).parent / "styles"


class Styles(Enum):
    """Enum for Matplotlib styles used in the project."""

    CMR10 = str(STYLES_DIR / "cmr10.mplstyle")
    ML = str(STYLES_DIR / "ml.mplstyle")
