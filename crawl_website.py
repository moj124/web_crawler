from gevent import monkey
monkey.patch_all()
import gevent
from collections import deque 
from urllib.parse import urlsplit
import requests
import sys
import argparse
import json
from bs4 import BeautifulSoup

class Crawler():
  def __init__(self,current_page):
    self.header= {'User-Agent': 'Mozilla/5.0'}
    self.current_page = current_page
    self.visited = set()
    self.local_links = set()
    self.foreign_links = set()
    self.broken_links = set()
    self.output = {}
    self.queue = deque([self.current_page])

  def get_links(self):
    try:
      while self.queue:
        url = self.queue.popleft()
        self.output[url] = []
        self.visited.add(url)
        print("Processing %s" % url)

        try:
            response = requests.head(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            # add broken urls to it's own set, then continue
            self.broken_links.add(url)
            continue
        try:
          req = requests.get(url)
        except:
          self.broken_links.add(url)
          continue
        
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        try:
          soup = BeautifulSoup(req.content, 'html.parser')
        except:
          self.broken_links.add(url)
          continue

        # extract link url from the anchor    
        for link in soup.find_all('a'): 
          anchor = link.attrs["href"] if "href" in link.attrs else ''
        
          if anchor.startswith('/'):        
            local_link = base_url + anchor
            self.output[url].append(local_link)         
            self.local_links.add(local_link)    
          elif strip_base in anchor:        

            self.output[url].append(anchor)
            self.local_links.add(anchor)    
          elif not anchor.startswith('http'):        
            local_link = path + anchor       

            self.output[url].append(local_link) 
            self.local_links.add(local_link)    
          else:        
            self.foreign_links.add(anchor)
        
        for i in self.local_links:    
          if not i in self.queue and not i in self.visited:          
            self.queue.append(i)
            self.output[url] = list(set(self.output[url]))
    except Exception as e:
      print(e)

  def run(self,numThreads):
    # while self.queue:
      threads = [gevent.spawn(self.get_links) for i in range(numThreads)]
      gevent.joinall(threads)


def main(argv):
    parser = argparse.ArgumentParser('The web_crawler is a asynchoronous gevent link crawler that maps all the associated local links constrained by the input webpage url.')
    parser.add_argument('--webpage','-l', type=str,
                        default='https://www.bbc.co.uk/', help='the starting webpage that the crawler will extract urls from')
    parser.add_argument('--threads','-n', type=int, default=3,
                        help='number of threads being used asynchronously')
    parser.add_argument('--savetofile','-s', type=bool, default=True,
                        help='save local link relations to json file')
    opt = parser.parse_args()
    print(opt)
    web_crawler = Crawler(opt.webpage)
    web_crawler.run(opt.threads)
    print()
    print(web_crawler.visited)
    print()
    print(web_crawler.local_links)
    print()
    print(web_crawler.foreign_links)
    print()
    print(web_crawler.broken_links)
    print()
    print(web_crawler.output)

    if opt.savetofile:
        parts = urlsplit(opt.webpage)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        with open(strip_base+'.json', 'w') as f:
            json.dump(web_crawler.output, f)

if __name__ == "__main__":
    main(sys.argv[1:])

