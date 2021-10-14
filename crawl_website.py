from gevent import monkey
monkey.patch_all()
import gevent
from collections import deque 
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup

class Crawler():
  def __init__(self,current_page):
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


        soup = BeautifulSoup(req.content, 'html.parser')
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
          if not i in self.queue and not i in self.visited:          self.queue.append(i)
        self.output[url] = list(set(self.output[url]))
    except Exception as e:
      print(e)

  def run(self,numThreads=3):
    # while self.queue:
      threads = [gevent.spawn(self.get_links) for i in range(numThreads)]
      gevent.joinall(threads)

url = "https://www.traackr.com/"
web_crawler = Crawler(url)
web_crawler.run(1000)
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

