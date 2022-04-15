import requests
from time import sleep, time
from bs4 import BeautifulSoup
from functools import wraps
from summoner import Summoner


def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        time_cost = time() - start_time
        print('' + func.__name__ + " func time_cost -> {:.3f}".format(time_cost))
        return result
    return clocked


def slist_page_extraction(slist_response):
    # EXTRACTION
    slist_html = slist_response.text
    slist_html = BeautifulSoup(slist_html, features='html.parser')
    ranking_table = slist_html.find(class_='ranking-table').tbody

    summoners = list()
    for tr in ranking_table.find_all('tr'):
        # sid
        sid = tr.get('id').strip('summoner-')
        summoner = Summoner(sid=sid)

        # rank
        td_rank = tr.find('td', class_='ranking-table__cell--rank')
        summoner.rank = int(td_rank.text)

        # name
        td_name = tr.find('td', class_='ranking-table__cell--summoner')
        summoner.name = td_name.find('span').text

        # tier
        td_tier = tr.find('td', class_='ranking-table__cell--tier')
        summoner.tier = td_tier.text.strip()

        # lp
        td_lp = tr.find('td', class_='ranking-table__cell--lp')
        summoner.lp = td_lp.text.strip().rstrip(' LP').replace(',', '')

        # level
        td_level = tr.find('td', class_='ranking-table__cell--level')
        summoner.level = int(td_level.text)

        # num of win
        div_win = tr.find(class_='winratio-graph__text--left')
        summoner.win = int(div_win.text) if div_win else 0

        # num of lose
        div_lose = tr.find(class_='winratio-graph__text--right')
        summoner.lose = int(div_lose.text) if div_lose else 0

        # ratio
        summoner.ratio = round(summoner.win/(summoner.win+summoner.lose), 2)
        summoners.append(summoner)
    return summoners


if __name__ == '__main__':
    @clock
    def main():
        summoners = list()
        clocked_get = clock(requests.get)
        start_page, target_page = 1, 500
        for page in range(start_page, target_page):
            # GET
            print('getting page', page)
            slist_response = clocked_get('https://www.op.gg/ranking/ladder/page={}'.format(page), verify=False)

            # EXTRACTION
            # summoner = slist_page_extraction(slist_response)
            # summoners.append(summoner)


    main()
    # 单线程500页面266秒。完成任务计算时间约5小时。
