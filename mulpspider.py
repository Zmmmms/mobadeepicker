import multiprocessing
import requests
from spide import clock, slist_page_extraction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def runner(url_queue):
    # DB conf
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/op", encoding='utf8',)
    dbsession = sessionmaker(bind=engine)
    session = dbsession()

    while url_queue.empty() is not True:
        url = url_queue.get()
        print('\r processing: {} / 33000'.format(33000-url_queue.qsize()))
        rsps = requests.get(url=url)
        url_queue.task_done()
        summoners = slist_page_extraction(rsps)
        session.add_all(summoners)
        session.commit()

    session.close()


@clock
def main():
    url_queue = multiprocessing.Manager().Queue()
    summoners_queue = multiprocessing.Manager().Queue()
    start_page, end_page = 1, 500

    for i in range(start_page, end_page):
        url_queue.put('https://www.op.gg/ranking/ladder/page=' + str(i))

    pool = multiprocessing.Pool(8)
    for _ in range(8):
        pool.apply_async(runner, args=(url_queue,))
    pool.close()
    pool.join()

    url_queue.join()


if __name__ == '__main__':
    # 并行500任务 6线程花费时间46秒，提高效率5.7倍左右。
    main()
