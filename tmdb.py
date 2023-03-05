import tmdbsimple as tmdb


tmdb.API_KEY = ""  # Get your own key please


class TVShows:
    def __init__(self):
        self.results = list()

    def search(self, query):
        search = tmdb.Search()
        search.tv(query=query)

        self.results.clear()

        for result in search.results:
            show = dict()
            show["name"] = result["name"]
            show["country"] = (
                result["origin_country"][0] if result["origin_country"] else None
            )
            show["year"] = result["first_air_date"].split("-")[0]
            show["id"] = result["id"]
            show["overview"] = result["overview"]
            self.results.append(show)


class TVShow:
    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.name = ""
        self.season_list = set()
        self.seasons = dict()

    def lookup_shows(self, name):
        shows = []

    def get_info(self):
        show = tmdb.TV(self.tmdb_id)
        response = show.info()

        self.name = show.name

        for season in show.seasons:
            self.season_list.add(season["season_number"])

    def get_season_info(self, season_number):
        if season_number in self.season_list:
            season = tmdb.TV_Seasons(self.tmdb_id, season_number)
            response = season.info()

            episodes = dict()

            for episode in season.episodes:
                episodes[episode["episode_number"]] = episode["name"]

            self.seasons[season_number] = episodes

    def filename(self, season_number, episode_number):
        # Season doesn't exist
        if season_number not in self.season_list:
            return None

        # Season exists, but we don't have the data for the season
        if season_number not in self.seasons:
            self.get_season_info(season_number)

        # Episode doesn't exist
        if episode_number not in self.seasons[season_number]:
            return None

        title = "{} - S{:02d}E{:02d} - {}".format(
            self.name,
            season_number,
            episode_number,
            self.seasons[season_number][episode_number],
        )

        return self.slugify(title)

    def slugify(self, string):

        illegal_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

        for char in illegal_chars:
            string = string.replace(char, "")

        return string
