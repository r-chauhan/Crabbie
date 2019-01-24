# Thread -> Worker; Queue -> Job

import threading
from queue import Queue
from crabbie import Crabbie
from domain import *
from general import *

PROJECT_NAME = '[project_name]'
HOMEPAGE = '[url]'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Crabbie(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die with main exit())
def create_workers():
    for _ in range (NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        # Process dies with main exit()
        t.daemon = True
        t.start()


# Do the next job in queue
def work():
    while True:
        url = queue.get()
        Crabbie.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Checks queue and crawls
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


# Execution
create_workers()
crawl()
