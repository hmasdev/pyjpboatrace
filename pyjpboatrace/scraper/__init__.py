from .base import BaseScraper
from .stadiums_scraper import StadiumsScraper
from .races_scraper import RacesScraper
from .race_info_scraper import RaceInfoScraper
from .just_before_info_scraper import JustBeforeInfoScraper
from .win_placeshow_odds_scraper import WinPlaceshowOddsScraper
from .quinellaplace_odds_scraper import QuinellaplaceOddsScraper
from .exacta_quinella_odds_scraper import ExactaQuinellaOddsScraper
from .trio_odds_scraper import TrioOddsScraper
from .trifecta_odds_scraper import TrifectaOddsScraper
from .result_scraper import ResultScraper

__all__ = [
    BaseScraper.__name__,
    StadiumsScraper.__name__,
    RacesScraper.__name__,
    RaceInfoScraper.__name__,
    JustBeforeInfoScraper.__name__,
    WinPlaceshowOddsScraper.__name__,
    QuinellaplaceOddsScraper.__name__,
    ExactaQuinellaOddsScraper.__name__,
    TrioOddsScraper.__name__,
    TrifectaOddsScraper.__name__,
    ResultScraper.__name__,
]
