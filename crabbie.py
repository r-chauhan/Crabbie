from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Crabbie:

    # Class variable (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Crabbie.project_name = project_name
        Crabbie.base_url = base_url
        Crabbie.domain_name = domain_name
        Crabbie.queue_file = Crabbie.project_name + '/queue.txt'
        Crabbie.crawled_file = Crabbie.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('Crabbie ' + str(len(Crabbie.queue)), Crabbie.base_url)

# Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Crabbie.project_name)
        create_data_file(Crabbie.project_name, Crabbie.base_url)
        Crabbie.queue = file_to_set(Crabbie.queue_file)
        Crabbie.crawled = file_to_set(Crabbie.crawled_file)

# Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Crabbie.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Crabbie.queue)) + ' | Crawled ' + str(len(Crabbie.crawled)))
            Crabbie.add_links_to_queue(Crabbie.gather_links(page_url))
            Crabbie.queue.remove(page_url)
            Crabbie.crawled.add(page_url)
            Crabbie.update_files()

# Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Crabbie.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

# Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Crabbie.queue:
                continue
            if url in Crabbie.crawled:
                continue
            if Crabbie.domain_name not in url:
                continue
            Crabbie.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crabbie.queue, Crabbie.queue_file)
        set_to_file(Crabbie.crawled, Crabbie.crawled_file)







