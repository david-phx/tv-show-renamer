import tmdbsimple as tmdb

from settings import Settings


class TVShow:
    """Retrieve and store TV show information from TMDB."""

    def __init__(self):
        """Initialize TVShow object."""
        self.settings = Settings()
        tmdb.API_KEY = self.settings["TMDB"]["api_key"]

        self.name = None
        self.tmdb_id = None
        self.season_list = set()
        self.episodes = dict()

    def search(self, query):
        """Search for TV shows matching query and return formatted list."""
        search = tmdb.Search()
        search.tv(query=query)

        show_list = list()

        for result in search.results:
            show = dict()
            show["name"] = result["name"]
            show["country"] = (
                result["origin_country"][0] if result["origin_country"] else None
            )
            show["year"] = result["first_air_date"].split("-")[0]
            show["id"] = result["id"]
            show["overview"] = result["overview"]
            show_list.append(show)

        return show_list

    def get_info(self, tmdb_id):
        """Get TV show name and season list by TMDB ID."""
        show = tmdb.TV(tmdb_id)
        show.info()

        self.name = show.name
        self.tmdb_id = tmdb_id

        self.season_list.clear()
        self.episodes.clear()

        for season in show.seasons:
            self.season_list.add(season["season_number"])

    def has_season(self, season_number):
        """Return True if season exists."""
        return season_number in self.season_list

    def get_season_info(self, season_number):
        """Get TV show season info."""

        if not self.has_season(season_number):
            return None

        season = tmdb.TV_Seasons(self.tmdb_id, season_number)
        season.info()

        episodes = dict()

        for episode in season.episodes:
            episodes[episode["episode_number"]] = episode["name"]

        self.episodes[season_number] = episodes

    def get_episode_name(self, season, episode):
        """Return episode name."""
        try:
            return self.episodes[season][episode]
        except KeyError:
            return ""
