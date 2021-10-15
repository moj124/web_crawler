from gevent import monkey
monkey.patch_all()
import gevent
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import random 
import requests
import argparse
import json
import time

class Crawler():
  def __init__(self,current_page):
    self.queue = [current_page]
    self.visited = set()
    self.local_links = set()
    self.foreign_links = set()
    self.broken_links = set()
    self.output = {}
  
  def get_next_link(self):
    if not self.queue:
      return None

    selected_index = random.choice(range(len(self.queue)))
    selected_link = self.queue[selected_index]
    del self.queue[selected_index]
    return selected_link

  def get_links(self):
    try:
      # Get a random link from the queue
      url = self.get_next_link()
      self.visited.add(url)
      
      # Document parent to child link relation
      self.output[url] = []
      print("Processing %s" % url)

      try:
        requests.head(url)
      except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        # add broken urls to it's own set, then continue
        self.broken_links.add(url)

      try:
        req = requests.get(url)
      except:
        # add unauthorized request from website response to it's own set, then continue
        self.broken_links.add(url)
  
      try:
        soup = BeautifulSoup(req.content, 'html.parser')
      except:
        self.broken_links.add(url)

      # extract sections of url to resolve relative links
      domain_name, webpage, path = getPartsOfURL(url)

      for link in soup.find_all('a'): 
        # extract link url from the anchor from <a> tag 
        anchor = link.attrs["href"] if "href" in link.attrs else ''
      
        # capture all links that have partially relative links, 
        # full links or links with parts and domain name
        # add all to local_links set
        if anchor.startswith('/'):
          # anchor contains a partial url link relative to the url      
          local_link = webpage + anchor

          # record the link url relation
          self.output[url].append(local_link)         
          self.local_links.add(local_link)    
        elif domain_name in anchor:   
          # record the link url relation
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
    start_time = time.time()
    while self.queue:
      threads = [gevent.spawn(self.get_links) for i in range(numThreads) if i+1 <= len(self.queue)]
      gevent.joinall(threads)
    print()
    print("--- %s seconds ---" % (time.time() - start_time))  

def getPartsOfURL(url):
  parts = urlsplit(url)
  base = "{0.netloc}".format(parts)

  domain_name = base.replace("www.", "")
  webpage = "{0.scheme}://{0.netloc}".format(parts)
  path = url[:url.rfind('/')+1] if '/' in parts.path else url
  return (domain_name,webpage,path)


def main():
    # description of the program
    parser = argparse.ArgumentParser('The web_crawler is a asynchoronous gevent link crawler that maps all the associated local links constrained by the input webpage url.')
    # the list of arguements avaliable
    parser.add_argument('--webpage','-l', type=str,
                        default='https://www.bbc.co.uk/', help='the starting webpage that the crawler will extract urls from')
    parser.add_argument('--threads','-n', type=int, default=1000,
                        help='number of threads being used asynchronously')
    parser.add_argument('--savetofile','-s', type=bool, default=False,
                        help='save local link relations to json file')

    # parse the terminal arguements for custom execution
    opt = parser.parse_args()

    # run the program with the given arguements
    web_crawler = Crawler(opt.webpage)
    web_crawler.run(opt.threads)

    # display results
    print("%d local links were found" % len(web_crawler.local_links))
    print("%d links were broken" % len(web_crawler.broken_links))

    if opt.savetofile:
        domain_name, webpage, path = getPartsOfURL(opt.webpage)
        with open(domain_name+'.json', 'w') as f:
            json.dump(web_crawler.output, f)
        print("Local link relations were saved to %s" % domain_name+'.json')
    else:
      print("Local link relations where not written to a json file")
    print("---------------------------------------------------------") 

if __name__ == "__main__":
  main()

