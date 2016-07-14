import spice
import helpers
from bs4 import BeautifulSoup

class Anime:
    """An object that encapsulates an Anime.

    Uses properties so that it doesn't parse through XML
    unnecessarily, and instead,  does so only when immediately
    necessary.

    Has properties:
        id         - The id of the anime.
        title      - The title of the anime.
        english    - The english name of the anime, if applicable.
        episodes   - The number of episodes in this anime.
        score      - The rating of the anime.
        anime_type - The type of anime (e.g. movie, ONA, etc)
        status     - In what state the anime is in (e.g. airing, finished, etc)
        dates      - A tuple of start and end dates of airing of the anime.
        synopsis   - The synopsis text of the anime.
        image_url  - A url to the anime's cover image.
    """
    def __init__(self, anime_data):
        self.raw_data = anime_data
        #these are generated when they are called, so we save
        #computation when it is not needed.
        self._id         = None
        self._title      = None
        self._english    = None
        self._episodes   = None
        self._score      = None
        self._anime_type = None
        self._status     = None
        self._dates      = None
        self._synopsis   = None
        self._image_url  = None
        self._rewatches  = None

    @property
    def id(self):
        if self._id is None:
            id_val = self.raw_data.id
            if id_val is None: #AnimeList Anime data.
                id_val = self.raw_data.series_animedb_id
            self._id = id_val.text
        return self._id

    @property
    def title(self):
        if self._title is None:
            title_val = self.raw_data.title
            if title_val is None:
                title_val = self.raw_data.series_title
            self._title = title_val.text
        return self._title

    @property
    def english(self):
        if self._english is None:
            english_val = self.raw_data.english
            if english_val is None:
                return None
            self._english = english_val.text
        return self._english

    @property
    def episodes(self):
        if self._episodes is None:
            episodes_val = self.raw_data.episodes
            if episodes_val is None:
                episodes_val = self.raw_data.my_watched_episodes
            self._episodes = episodes_val.text
        return self._episodes

    @property
    def score(self):
        if self._score is None:
            score_val = self.raw_data.score
            if score_val is None:
                score_val = self.raw_data.my_score
            self._score = score_val.text
        return self._score

    @property
    def anime_type(self):
        if self._type is None:
            type_val = self.raw_data.type
            if type_val is None:
                return None
            self._type = type_val.text
        return self._type

    @property
    def status(self):
        if self._status is None:
            status_val = self.raw_data.status
            if status_val is None:
                status_val = self.raw_data.my_status
            self._status = status_val.text
        return self._status

    @property
    def dates(self):
        if self._dates is None:
            start_val = self.raw_data.start_date
            end_val = self.raw_data.end_date
            if start_val is None:
                start_val = self.raw_data.my_start_date
                end_val = self.raw_data.my_end_date
            self._dates = (start_val.text, end_val.text)
        return self._dates

    @property
    def synopsis(self):
        if self._synopsis is None:
            synopsis_val = self.raw_data.synopsis
            if synopsis_val is None:
                return None
            self._synopsis = synopsis_val.text
        return self._synopsis

    @property
    def image_url(self):
        if self._image_url is None:
            image_val = self.raw_data.image
            if image_val is None:
                return Non
            self._image_url = image_val.text
        return self._image_url

    @property
    def rewatches(self):
        if self._rewatches is None:
            rewatch_val = self.raw_data.my_rewatching
            if rewatch_val is None:
                return None
            self._rewatches = rewatch_val.text
            return self._rewatches

    @property
    def rewatch_ep(self):
        if self._rewatch_ep is None:
            rewatch_ep_val = self.raw_data.my_rewatching_ep
            if rewatch_ep_val is None:
                return None
            self._rewatch_ep = rewatch_ep_val.text
            return self._rewatch_ep

class AnimeData:
    """An object for packaging data required for operations on AnimeLists

    Has properties:
        episodes - The number of episodes in this anime that you've watched.
        status   - Are you: watching(1), completed(2), on-hold(3), dropped(4),
                          plan-to-watch(6) <- Don't ask me, ask MAL devs >_>.
        score    - The rating of the anime.
        dates    - A tuple of start and end dates of airing of the anime.
        tags     - The tags to put on your list for this Anime.
        The rest are not necessary for operations and can be left blank.
    """
    def __init__(self):
        self.episodes = 0
        self.status = 0
        self.score = 0
        self.storage_type = ''
        self.storage_value = ''
        self.times_rewatched = ''
        self.rewatch_value = ''
        self.dates = ('', '')
        self.priority = ''
        self.set_discuss = ''
        self.set_rewatch = ''
        self.comments = ''
        self.fansub_group = ''
        self.tags = []

    def to_xml(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
                <entry>
                    <episode>{}</episode>
                    <status>{}</status>
                    <score>{}</score>
                    <storage_type>{}</storage_type>
                    <storage_value>{}</storage_value>
                    <times_rewatched>{}</times_rewatched>
                    <rewatch_value>{}</rewatch_value>
                    <date_start>{}</date_start>
                    <date_finish>{}</date_finish>
                    <priority>{}</priority>
                    <enable_discussion>{}</enable_discussion>
                    <enable_rewatching>{}</enable_rewatching>
                    <comments>{}</comments>
                    <fansub_group>{}</fansub_group>
                    <tags>{}</tags>
                </entry>""".format(self.episodes, self.status,
                                   self.score, self.storage_type,
                                   self.storage_value, self.times_rewatched,
                                   self.rewatch_value, self.dates[0],
                                   self.dates[1], self.priority,
                                   self.set_discuss, self.set_rewatch,
                                   self.comments, self.fansub_group,
                                   str(self.tags)[1:-1].replace('\'', ''));


class Manga:
    """An object that encapsulates an Manga.

    Uses properties so that it doesn't parse through XML
    unnecessarily, and instead,  does so only when immediately
    necessary.

    Has properties:
        id         - The id of the manga.
        title      - The title of the manga.
        english    - The english name of the manga, if applicable.
        chapter    - The number of chapters in this manga.
        volume     - The number of volumes in this manga.
        score      - The rating of the manga.
        manga_type - The type of manga (e.g. movie, ONA, etc)
        status     - In what state the manga is in (e.g. airing, finished, etc)
        dates      - A tuple of start and end dates of airing of the manga.
        synopsis   - The synopsis text of the manga.
        image_url  - A url to the manga's cover image.
    """
    def __init__(self, manga_data):
        self.raw_data = manga_data
        self._id = None
        self._title = None
        self._english = None
        self._chapter = None
        self._volume = None
        self._score = None
        self._type = None
        self._status = None
        self._dates = None
        self._synopsis = None
        self._image_url = None

    @property
    def id(self):
        if self._id is None:
            self._id = self.raw_data.id.text
        return self._id

    @property
    def title(self):
        if self._title is None:
            self._title = self.raw_data.title.text
        return self._title

    @property
    def english(self):
        if self._english is None:
            self._english = self.raw_data.english.text
        return self._english

    @property
    def episodes(self):
        if self._episodes is None:
            self._episodes = self.raw_data.episodes.text
        return self._episodes

    @property
    def score(self):
        if self._score is None:
            self._score = self.raw_data.score.text
        return self._score

    @property
    def manga_type(self):
        if self._type is None:
            self._type = self.raw_data.type.text
        return self._type

    @property
    def status(self):
        if self._status is None:
            self._status = self.raw_data.status.text
        return self._status

    @property
    def dates(self):
        if self._dates is None:
            start_date = self.raw_data.start_date.text
            end_date = self.raw_data.end_date.text
            self._dates = (start_date, end_date)
        return self._dates

    @property
    def synopsis(self):
        if self._synopsis is None:
            self._synopsis = self.raw_data.synopsis.text
        return self._synopsis

    @property
    def image_url(self):
        if self._image_url is None:
            self._image_url = self.raw_data.image.text
        return self._image_url

class MangaData:
    """An object for packaging data required for operations on MangaLists

    Has properties:
        chapters - The number of chapters in this manga that you've read.
        volume   - The volume in this manga that you've read.
        status   - Are you: reading(1), completed(2), on-hold(3), dropped(4),
                          plan-to-read(6) <- Don't ask me, ask MAL devs >_>.
        score    - The rating of the manga.
        dates    - A tuple of start and end dates of airing of the manga.
        tags     - The tags to put on your list for this manga.
        The rest are not necessary for operations and can be left blank.
    """
    def __init__(self):
        self.chapters = 0
        self.volume = 0
        self.status = 0
        self.score = 0
        self.times_reread = ''
        self.reread_value = ''
        self.dates = ('', '')
        self.priority = ''
        self.set_discuss = ''
        self.set_reread = ''
        self.comments = ''
        self.scan_group = ''
        self.tags = []
        self.retail_volumes = ''

    def to_xml(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
                <entry>
                    <chapter>{}</chapter>
                    <volume>{}</volume>
                    <status>{}</status>
                    <score>{}</score>
                    <times_reread>{}</times_reread>
                    <reread_value>{}</reread_value>
                    <date_start>{}</date_start>
                    <date_finish>{}</date_finish>
                    <priority>{}</priority>
                    <enable_discussion>{}</enable_discussion>
                    <enable_rereading>{}</enable_rereading>
                    <comments>{}</comments>
                    <scan_group>{}</scan_group>
                    <tags>{}</tags>
                    <retail_volumes>{}</retail_volumes>
                </entry>""".format(self.chapters, self.volumes,
                                   self.status, self.score, self.times_reread,
                                   self.reread_value, self.dates[0],
                                   self.dates[1], self.priority,
                                   self.set_discuss, self.set_reread,
                                   self.comments, self.scan_group,
                                   str(self.tags)[1:-1].replace('\'', ''),
                                   self.retail_volumes);

class MediumList:
    def __init__(self, medium, list_data):
        self.medium = medium
        self.raw_data = list_data
        if self.medium == spice.Medium.ANIME:
            self.anime_list = {'watching':[], 'completed':[], 'onhold':[],
                           'dropped':[], 'plantowatch':[]}
        elif self.medium == spice.Medium.MANGA:
            self.manga_list = {'reading':[], 'completed':[], 'onhold':[],
                           'dropped':[], 'plantoread':[]}
        else:
            #not sure what the best thing to do is... default to anime?
            raise ValueError(constants.INVALID_MEDIUM)

        self.load()

    def load(self):
        list_soup = BeautifulSoup(self.raw_data, 'lxml')
        if self.medium == spice.Medium.ANIME:
            list_items = list_soup.findAll('anime')
            for item in list_items:
                status = helpers.find_key(item.my_status.text, self.medium)
                status_list = self.anime_list[status]
                status_list.append(Anime(item))
                print(item.series_title)
        else: #we are guaranteed to, at this point, have a valid medium
            list_items = list_soup.findAll('manga')
            for item in list_items:
                status = helpers.find_key(item.my-status.text, self.medium)
                status_list = self.manga_list[status]
                status_list.append(Manga(item))
