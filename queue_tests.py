import pytest
from crawl_website import Crawler

@pytest.fixture
def starting_queue():
    crawl = Crawler('https://example.com/')
    return crawl

def test_starting_elements_queue(starting_queue):
    empty_first_link = starting_queue.get_next_link()
    empty_second_link = starting_queue.get_next_link()
    assert empty_first_link == 'https://example.com/'
    assert empty_second_link == None

def test_starting_length_queue(starting_queue):
    assert len(starting_queue.queue) == 1
    starting_queue.get_next_link()
    assert len(starting_queue.queue) == 0

@pytest.mark.parametrize("full_queue",[
    ["https://www.scrapethissite.com/faq/",
    "https://www.scrapethissite.com/", 
    "https://www.scrapethissite.com/lessons/", 
    "https://www.scrapethissite.com/pages/", 
    "https://www.scrapethissite.com/login/"]
])
def test_full_queue(full_queue,starting_queue):
    starting_queue.queue = full_queue
    assert len(starting_queue.queue) == 5
    selected_link = starting_queue.get_next_link()
    assert selected_link not in starting_queue.queue
    assert len(starting_queue.queue) == 4

@pytest.mark.parametrize("empty_queue",[
    []
])
def test_empty_queue(empty_queue,starting_queue):
    starting_queue.queue = empty_queue
    assert len(starting_queue.queue) == 0
    selected_link = starting_queue.get_next_link()
    assert selected_link == None
