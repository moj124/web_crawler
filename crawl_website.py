from gevent import joinall, spawn, monkey
monkey.patch_all()
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import random 
import requests
import argparse
import sys
import json
import time


class Crawler():
  """
  A class used to represent an web crawler

  Attributes
  ----------
  queue : array
      contains links local to the current_page that are yet to be visited as strings
  visited : set
      the set of all local links that have been visited
  local_links : set
    the set of all links local to the current url being processed
  broken_links : set
    the set of all local links that couldn't be visited due to errors
  output : dictionary
      a dictionary containing the relations between parent and child pages

  Methods
  -------
  get_next_link()
      randomly selects a link from the queue
  get_links()
      scrapes the selected link from get_next_link webpage for other local links
  run()
      runs get_links() asynchronously until all links from the queue are visited
  """
  def __init__(self,current_page):
    """
      Parameters
      ----------
      current_page : string
          base webpage to search for all local links related to the base webpage's domain
    """
    self.queue = [current_page]
    self.visited = set()
    self.local_links = set()
    self.broken_links = set()
    self.output = {}
  
  def get_next_link(self):
    """ Randomly selects a link from the queue
    
    Raises
    ------
    None
        If queue is empty.
    """

    # check if queue is not empty
    if not self.queue:
      return None

    # select one link from the queue of links
    selected_index = random.choice(range(len(self.queue)))
    selected_link = self.queue[selected_index]

    # delete the selected link from the queue of links
    del self.queue[selected_index]
    return selected_link

  def get_links(self):
    """ Scrapes the selected link from get_next_link webpage for other local links"""
    start_time = time.time()
    try:
      # Get a random link from the queue
      try:
        url = self.get_next_link()
      except None as e:
        print("no link generated")  
      self.visited.add(url)
      
      # Document parent to child link relation
      self.output[url] = []
      print("Processing %s" % url)

      try:
        requests.head(url)
      except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        # add broken urls to it's own set, then continue
        self.broken_links.add(url)
        print("request failed")    

      try:
        req = requests.get(url)
      except:
        # add unauthorized request from website response to it's own set, then continue
        self.broken_links.add(url)
        print("unauthorised get request")  
  
      try:
        soup = BeautifulSoup(req.content, 'html.parser')
      except:
        self.broken_links.add(url)
        print("failed to read body")  

      # extract sections of url to resolve relative links
      domain_name, webpage, path = get_parts_of_url(url)

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
          # anchor contains a partial url link relative to the url or domain and part    
          local_link = path + anchor      

          # record the link url relation
          self.output[url].append(local_link) 
          self.local_links.add(local_link)    
      
      # add all unvisited and not in the queue links from the local_links
      for i in self.local_links:    
        if not i in self.queue and not i in self.visited:          
          self.queue.append(i)
          self.output[url] = list(set(self.output[url]))

    except Exception as e:
      # unknown error has occured
      print(e)

  def run(self,maximum_threads):
    """Runs get_links() asynchronously until all links from the queue are visited

    Parameters
    ----------
    maximum_threads : int
        Specifies the maxmium number of threads that can be spawned
    """

    # record the time performance of the program
    start_time = time.time()

    # continuously spawn threads of get_links 
    # until there are no more links to visit
    while self.queue:
      # spawn threads according to the queue length and defined max thread count
      threads = [spawn(self.get_links) for i in range(maximum_threads) if i+1 <= len(self.queue)]
      # await until threads finish execution
      joinall(threads,timeout=2)
    print()
    print("--- %s seconds ---" % (time.time() - start_time))  

def get_parts_of_url(url):
  """Parses the url and return a selection of formatted strings for domain name, webpage and relative path

    Parameters
    ----------
    url : string
        a webpage link to be parsed into relevant parts for web crawling
  """
  # parse url into relevant parts
  parts = urlsplit(url)
  # print(parts)
  # format specific sections of the url for domain_name, webpage and relative paths
  base = "{0.netloc}".format(parts)
  domain_name = base.replace("www.", "")
  webpage = "{0.scheme}://{0.netloc}".format(parts)
  path = url[:url.rfind('/')+1] if '/' in parts.path else url
  return (domain_name,webpage,path)


def main():
    """Runs the web crawler asynchronously to collect data on the local links and their relations"""
    # description of the program
    parser = argparse.ArgumentParser('The web_crawler is a asynchronous gevent link crawler that maps all the associated local links constrained by the input webpage url.')
    # the list of arguements avaliable
    parser.add_argument('--webpage','-l', type=str,
                        default='https://www.bbc.co.uk/', help='the starting webpage that the crawler will extract urls from')
    parser.add_argument('--maximum_threads','-n', type=int, default=1000,
                        help='number of threads being used asynchronously')
    parser.add_argument('--savetofile','-s', type=bool, default=False,
                        help='save local link relations to json file')
    parser.add_argument('--data_directory','-d', type=str, default='data/',
                        help='directory to save the file to')

    # parse the terminal arguements for custom execution
    opt = parser.parse_args()
    # run the program with the given arguements
    web_crawler = Crawler(opt.webpage)
    web_crawler.run(opt.maximum_threads)

    # display results
    print("%d local links were found" % len(web_crawler.local_links))
    print("%d links were broken" % len(web_crawler.broken_links))

    if opt.savetofile:
        domain_name, webpage, path = get_parts_of_url(opt.webpage)
        with open(opt.data_directory+domain_name+'.json', 'w') as f:
            json.dump(web_crawler.output, f)
        print("Local link relations were saved to %s" % ('./'+opt.data_directory+domain_name+'.json'))
    else:
      print("Local link relations where not written to a json file")
    print("---------------------------------------------------------") 

if __name__ == "__main__":
  main()

