import time
import requests
from threading import Thread, Semaphore
import random
from requests_func import get_descriptoin, get_part_description, open_file_articles, open_file_proxy, write_data

s = Semaphore(100)  # Threads
threads = []
data = dict()
delay = 0.2  # Delay


def main_func(proxy, article):
    try:
        s.acquire()
        proxy_url = f"http://{proxy}"
        session = requests.Session()
        session.proxies = {'http': proxy_url, 'https': proxy_url}
        description = get_descriptoin(article, session)
        status, part_description = get_part_description(article, session)
        if status == False:
            part_description = description
        data[article] = [description, part_description]
        session.close()
        time.sleep(delay)

    finally:
        s.release()


if __name__ == "__main__":
    article_list = open_file_articles()
    proxy_list = open_file_proxy()

    for article in article_list:
        proxy = random.choice(proxy_list)
        t = Thread(target=main_func, args=(proxy, article))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    write_data(article_list, data)
