# driver code

from fspy.scrapper import *
from fspy.scrapper import VERBOSITY_LEVEL_DEBUG

"""
    Driver code 
    ----------------
"""
if __name__ == '__main__':
    scrapper_NFL = FlashScrapper("nfl.csv", 2000, 2023,
                             "american-football", "usa", "nfl",
                                 verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_premier_league = FlashScrapper("premier_league.csv", 2000, 2023,
                                 "football", "england", "premier-league",
                                            verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_NBA = FlashScrapper("nba.csv", 2000, 2023,
                                 "basketball", "usa", "nba", verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_extra_liga = FlashScrapper("extra_liga.csv", 2000, 2023,
                                 "hockey", "czech-republic", "extra-liga",
                                        verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_wimbledon = FlashScrapper("wimbledon.csv", 2000, 2023,
                                 "tennis", "wta-singles", "wimbledon", has_seasons=False,
                                       verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_svenska_superligan = FlashScrapper("svenska_superligan.csv", 2000, 2023,
                                       "floorball", "sweden", "svenska-superligan",
                                                verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_plusliga = FlashScrapper("plusliga.csv", 2008, 2023,
                                                "volleyball", "poland", "plusliga",
                                      verbosity_level=VERBOSITY_LEVEL_DEBUG)

    scrapper_NFL.run()
    scrapper_premier_league.run()
    scrapper_NBA.run()
    scrapper_extra_liga.run()
    scrapper_wimbledon.run()
    scrapper_svenska_superligan.run()
    scrapper_plusliga.run()


