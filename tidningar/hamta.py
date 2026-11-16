"""Krav: K37 i KRAV.md och den artiga hämtningen i KALLOR.md.

Läser robots.txt före flödet, säger vem vi är i User-Agent och väntar
mellan anropen. Saknas robots.txt är allt tillåtet. Ett svar som inte är
200 hämtas inte om; felet går vidare till rapporten.
"""

import time
import urllib.error
import urllib.request
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

AGENT = "Giffa-bevakning/1.0 (+https://github.com/moggleif/giffa)"
PAUS = 5


def hamta(adress: str) -> str:
    robots = RobotFileParser()
    robots.parse(robotsrader(urljoin(adress, "/robots.txt")))
    if not robots.can_fetch(AGENT, adress):
        raise PermissionError("robots.txt spärrar flödet")
    time.sleep(PAUS)
    return oppna(adress)


def robotsrader(adress: str) -> list[str]:
    try:
        return oppna(adress).splitlines()
    except urllib.error.HTTPError as fel:
        if fel.code != 404:
            raise
        return []


def oppna(adress: str) -> str:
    fraga = urllib.request.Request(adress, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(fraga, timeout=30) as svar:
        return svar.read().decode("utf-8")
