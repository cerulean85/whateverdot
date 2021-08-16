import json
from urllib import parse
from selenium import webdriver

# IP_DIRECTOR = "localhost"
# PORT_DIRECTOR = 8084
#
# IP_WORKER = "localhost"
# PORT_WORKER = 8085

# KEYWORD = "코로나_백신"
# START_DATE = "2021-02-26"
# END_DATE = "2021-06-30"
# START_DATE = "2020-01-01"
# END_DATE = "2020-08-31"

# FACEBOOK_START_YEAR = "2020"
# FACEBOOK_END_YEAR = "2021"
#
# INSTAGRAM_DELAY_TIME = 3
# SAVE_DIR = "D:/__programming/wed_storage/"
# CHROME_PATH = "C:/chromedriver_win32/chromedriver.exe"
# DELAY_SECONDS = 5
#
#
# INSTAGRAM_DOMAIN = "https://www.instagram.com/"
# INSTAGRAM_ACCOUNT_ID = "zhwan85@gmail.com"
# INSTAGRAM_ACCOUNT_PASS = "!Wlsghks39682"

def get_config(path=''):
    with open(path + "config.json", "r") as st_json:
        conf = json.load(st_json)

    return conf


def get_chrome_driver(config_path=''):

    conf = get_config(path=config_path)
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('disable-gpu')
    options.set_capability('unhandledPromptBehavior', 'accept')
    options.add_argument("--use-fake-ui-for-media-stream")
    return webdriver.Chrome(conf["chrome_driver"]["path"], options=options)


def get_probe_url(channel, keyword, startDate, endDate, config_path=''):
    assert (channel != '' and channel is not None)

    conf = get_config(path=config_path)
    seed = conf[channel]["seed"]["probe"]
    if channel == 'chs':
        encQuery = parse.quote(keyword).replace('_', ' ')
        startDate = startDate.replace('-', '')
        endDate = endDate.replace('-', '')
        dot_startDate = startDate[0:4] + '.' + startDate[4:6] + '.' + startDate[6:8]
        dot_endDate = endDate[0:4] + '.' + endDate[4:6] + '.' + endDate[6:8]
        return seed % (encQuery, startDate, endDate, dot_startDate, dot_endDate)

    elif channel == 'dna':
        encQuery = parse.quote(keyword)
        encQuery = encQuery.replace('_', ' ')
        startDate = startDate.replace('-', '')
        endDate = endDate.replace('-', '')
        return seed % (startDate, endDate, encQuery)

    elif channel == 'jna':
        encQuery = parse.quote(keyword).replace('_', ' ')
        startDate = startDate.replace('-', '.')
        endDate = endDate.replace('-', '.')
        return seed % (startDate, endDate, encQuery)

    elif channel == 'nav':
        encQuery = parse.quote(keyword).replace('_', ' ')
        return seed % (startDate, endDate, encQuery)

    return ''

def get_collect_url(channel, pageCount, keyword, startDate, endDate, config_path=''):
    assert (channel != '' and channel is not None)

    conf = get_config(path=config_path)
    seed = conf[channel]["seed"]["collect"]
    if channel == 'chs':
        encQuery = parse.quote(keyword).replace('_', ' ')
        startDate = startDate.replace('-', '')
        endDate = endDate.replace('-', '')
        dot_startDate = startDate[0:4] + '.' + startDate[4:6] + '.' + startDate[6:8]
        dot_endDate = endDate[0:4] + '.' + endDate[4:6] + '.' + endDate[6:8]
        return seed % (encQuery, startDate, endDate, dot_startDate, dot_endDate)

    elif channel == 'dna':
        encQuery = parse.quote(keyword).replace('_', ' ')
        startDate = startDate.replace('-', '')
        endDate = endDate.replace('-', '')
        return seed % (str((pageCount - 1) * 15 + 1), encQuery, startDate, endDate)

    elif channel == 'jna':
        encQuery = parse.quote(keyword).replace('_', ' ')
        startDate = startDate.replace('-', '')
        endDate = endDate.replace('-', '')
        startDate = startDate[4:6] + '/' + startDate[6:8] + '/' + startDate[0:4] + ' 00:00:00'
        endDate = endDate[4:6] + '/' + endDate[6:8] + '/' + endDate[0:4] + ' 00:00:00'
        return seed % (str(pageCount), encQuery, startDate, endDate)

    elif channel == 'nav':
        encQuery = parse.quote(keyword).replace('_', ' ')
        return seed % (pageCount, startDate, endDate, encQuery)

    return ''


# seedProbe = {
#     "donga": "https://www.donga.com/news/search?check_news=1&more=1&sorting=1&range=1&search_date=5&v1=%s&v2=%s&query=%s",
#     "joongang": "https://news.joins.com/Search/JoongangNews?StartSearchDate=%s&EndSearchDate=%s&Keyword=%s&SortType=New&SearchCategoryType=JoongangNews&PeriodType=DirectInput&ScopeType=All&ServiceCode=&SourceGroupType=&ReporterCode=&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&MatchKeyword=&IncludeKeyword=&ExcluedeKeyword=",
#     "chosun": "https://search.naver.com/search.naver?where=news&query=%s&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=%s&de=%s&docid=&nso=so:r,p:from%sto%s,a:all&mynews=1&refresh_start=0&related=0",
#     "naver_blog": "https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=PERIOD&orderBy=date&startDate=%s&endDate=%s&keyword=%s"
#     # "chosun": "https://search.naver.com/search.naver?where=news&query=%s&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=%s&de=%s&docid=&mynews=1&refresh_start=0&related=0"
# }
#
# seedCollect = {
#     "donga": "https://www.donga.com/news/search?p=%s&query=%s&check_news=1&more=1&sorting=1&range=1&search_date=5&v1=%s&v2=%s",
#     "chosun": "https://search.naver.com/search.naver?where=news&query=%s&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=%s&de=%s&docid=&nso=so:r,p:from%sto%s,a:all&mynews=1&refresh_start=0&related=0",
#     "joongang": "https://news.joins.com/Search/JoongangNews?page=%s&Keyword=%s&PeriodType=DirectInput&StartSearchDate=%s&EndSearchDate=%s&SortType=New&SearchCategoryType=JoongangNews",
#     "naver_blog": "https://section.blog.naver.com/Search/Post.nhn?pageNo=%s&rangeType=PERIOD&orderBy=date&startDate=%s&endDate=%s&keyword=%s"
# }





