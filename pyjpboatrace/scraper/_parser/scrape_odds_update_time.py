from logging import Logger, getLogger

from bs4 import BeautifulSoup

_logger: Logger = getLogger(__name__)

def scrape_odds_update_time(
    soup: BeautifulSoup,
    logger: Logger = _logger,
) -> str:

    # case: after time-limit
    ps = soup.select("p.tab4_time")
    if ps:
        if len(ps) >= 2:
            logger.warning(f"# of p.tab4_time should be 1 but {len(ps)}")
        p = ps[0]
        return p.text

    # case: before time-limit
    ps = soup.select("p.tab4_refreshText")
    if ps:
        if len(ps) >= 2:
            logger.warning(f"# of p.tab4_refreshText should be 1 but {len(ps)}")  # noqa
        p = ps[0]
        return p.text.split()[-1]  # Suppose that p.text == "オッズ更新時間　9:02"

    logger.warning("Failed to find the update timestamp")
    return "Failed to find the update timestamp"
