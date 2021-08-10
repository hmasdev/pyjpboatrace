from bs4 import BeautifulSoup


def scrape_odds_update_time(soup: BeautifulSoup) -> str:

    # case: after time-limit
    ps = soup.select("p.tab4_time")
    if ps:
        # TODO warn when len(ps) >= 2
        p = ps[0]
        return p.text

    # case: before time-limit
    ps = soup.select("p.tab4_refreshText")
    if ps:
        # TODO warn when len(ps) >= 2
        p = ps[0]
        return p.text.split()[-1]  # Suppose that p.text == "オッズ更新時間　9:02"

    # TODO logger
    return "Failed to find the update timestamp"
