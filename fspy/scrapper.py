"""
    Name: scrapper.py
    Author: Jakub Sukdol
    Date: 04.12.24

    Scrapper Class for scrapping flashscore.com
    (Only for educational and Data Science purposes!!)

    Note that this scrapper only acquires the final results of the matches
    as present in the flashscore archive (e.g. https://www.flashscore.com/american-football/usa/nfl-2023-2024/results/)
"""

__all__ = ["FlashScrapper"]

import pandas as pd
from typing import Optional, Final
import time
import re
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

VERBOSITY_LEVEL_NONE: Final[int] = 0
VERBOSITY_LEVEL_INFO: Final[int] = 1
VERBOSITY_LEVEL_DEBUG: Final[int] = 2


class FlashScrapper:
    """
    FlashScrapper Class for scrapping flashscore.com

    :param out_path: (str) path to save the scrapped dataframe as csv
    :param start_year: (int) lower year of the first season
    :param end_year: (int) higher year of the last season
    :param has_seasons: (bool) the format of seasons is YYYY-YYYY if true else YYYY
    """
    def __init__(self, out_path: str, start_year: int, end_year: int, sport: str, country: str, league: str,
                 has_seasons: bool = True, verbosity_level: int = 0):
        self._out_path: str = out_path

        self._start_year: int = start_year
        self._end_year: int = end_year

        self._base_url: str = "https://www.flashscore.com/" + sport + "/" + country + "/" + league
        self._url = ""

        self._has_seasons: bool = has_seasons
        self._country: str = country
        self._league: str = league

        self._verbosity_level: bool = verbosity_level

        self._df: pd.DataFrame = pd.DataFrame({"DT": [], "Home": [], "Away": [], "Home_points": [], "Away_points": [], "season": [], "country": [], "league": []})
        self._driver: Optional[WebDriver] = None

    def _safe_data_csv(self):
        self._df.to_csv(self._out_path, index=False)
        if self._verbosity_level >= VERBOSITY_LEVEL_INFO:
            print(f"[INFO] Saving {self._league} data to {self._out_path}")

    def _create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        driver = Chrome(options=options)
        driver.implicitly_wait(3)
        driver.get(self._url)

        # give driver time to load the page
        time.sleep(1)
        return driver

    def _load_whole_page(self):
        """ driver has to be created before calling this method """
        driver = self._driver

        if self._verbosity_level >= VERBOSITY_LEVEL_DEBUG:
            print("[DEBUG] Scrolling to the bottom of the page")

        while True:
            try:
                more = driver.find_element(
                    By.CLASS_NAME, "event__more.event__more--static"
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView();arguments[1].click();",
                    more,
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(more)),
                )
                time.sleep(2)  # give driver time to load the page
            except Exception as e:
                # print(f"[INFO] {e}")
                # no clickable element for loading more data on page found
                break

    def _run_one_season(self, season: str):
        """ run the scrapper and save the data to path specified in the init """
        self._url = self._base_url + "-" + season + "/results/"

        if self._verbosity_level >= VERBOSITY_LEVEL_INFO:
            print(f"[INFO] scrapping data from {self._url}")

        self._driver = self._create_driver()
        self._load_whole_page()

        html = self._driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        home_score = soup.find_all(class_="event__score event__score--home")
        home_score = list(map(lambda x: int(x.contents[0]), home_score))
        away_score = soup.find_all(class_="event__score event__score--away")
        away_score = list(map(lambda x: int(x.contents[0]), away_score))

        home_participant = soup.find_all("div", {"class" : re.compile('event__participant event__participant--home.*')})
        home_participant = list(map(lambda x: x.contents[0], home_participant))
        away_participant = soup.find_all("div", {"class" : re.compile('event__participant event__participant--away.*')})
        away_participant = list(map(lambda x: x.contents[0], away_participant))

        season_array = [season for _ in range(len(home_score))]
        league_array = [self._league for _ in range(len(home_score))]
        country_array = [self._country for _ in range(len(home_score))]

        if not home_participant:
            # probably premier league
            participants = soup.find_all(class_=re.compile('wcl-simpleText_Asp-0 wcl-scores-simpleText-01_pV2Wk.*'))
            for i in range(len(participants)):
                if i % 2 == 0:
                    home_participant.append(participants[i].contents[0])
                else:
                    away_participant.append(participants[i].contents[0])

        dt = soup.find_all(class_="event__time")
        dt = list(map(lambda x: x.contents[0], dt))

        season_years =  season.split("-") if "-" in season else season
        for i in range(len(dt)):
            if isinstance(season_years, list):
                year = season_years[1] if int(dt[i][3:5]) < 7 else season_years[0]
            else:
                year = season_years
            dt[i] = dt[i][:6] + year + dt[i][6:]

        dt = list(map(lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M"), dt))

        df = pd.DataFrame({"DT": dt, "Home": home_participant, "Away": away_participant, "Home_points": home_score,
                           "Away_points": away_score, "season": season_array, "country": country_array, "league": league_array})

        self._df = pd.concat([df, self._df], axis=0, ignore_index=True)

        if self._verbosity_level >= VERBOSITY_LEVEL_DEBUG:
            print(f"[DEBUG] total number of matches scrapped: {len(self._df)}")


    def run(self):
        while self._start_year < self._end_year:
            if self._has_seasons:
                season = str(self._start_year) + "-" + str(self._start_year + 1)
            else:
                season = str(self._start_year)

            if self._verbosity_level >= VERBOSITY_LEVEL_INFO:
                print(f"[INFO] scrapping {self._league} season {season}")

            self._run_one_season(season)
            self._start_year += 1

        self._safe_data_csv()
