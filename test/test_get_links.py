import pytest
from ..crawl_website import Crawler

@pytest.mark.parametrize("links",[
    ["https://www.loginradius.com/",
    "https://example.com/", 
    "https://www.scrapethissite.com/"
    ]
])
def test_link_web_scrape(links):
    web_crawler = Crawler(links[0])
    web_crawler.run(100)
    assert len(web_crawler.visited) == 1
    assert len(web_crawler.broken_links) == 0
    web_crawler = Crawler(links[1])
    web_crawler.run(100)
    assert len(web_crawler.visited) == 1
    assert len(web_crawler.broken_links) == 0
    web_crawler = Crawler(links[2])
    web_crawler.run(100)
    assert len(web_crawler.visited) == 39
    assert len(web_crawler.broken_links) == 0

@pytest.mark.parametrize("links",[
    ["https://www.loginradius.com/",
    "https://example.com/", 
    "https://www.scrapethissite.com/"
    ]
])
def test_number_of_threads_and_timeout_link_web_scrape(links):
    web_crawler = Crawler(links[0])
    with pytest.raises(ValueError):
        web_crawler.run(0)
        
    web_crawler = Crawler(links[1])
    with pytest.raises(ValueError):
        web_crawler.run(0)
    web_crawler = Crawler(links[2])
    with pytest.raises(ValueError):
        web_crawler.run(0)

    web_crawler = Crawler(links[0])
    with pytest.raises(ValueError):
        web_crawler.run(0,0)
    web_crawler = Crawler(links[1])
    with pytest.raises(ValueError):
        web_crawler.run(0,0)
    web_crawler = Crawler(links[2])
    with pytest.raises(ValueError):
        web_crawler.run(0,0)

    web_crawler = Crawler(links[0])
    with pytest.raises(ValueError):
        web_crawler.run(100,0)
    web_crawler = Crawler(links[1])
    with pytest.raises(ValueError):
        web_crawler.run(100,0)
    web_crawler = Crawler(links[2])
    with pytest.raises(ValueError):
        web_crawler.run(100,0)

@pytest.mark.parametrize("links",[
    ["https://www.loginradius.com/",
    "https://example.com/"
    ]
])
def test_length_link_web_scrape(links):
    web_crawler = Crawler(links[0])
    web_crawler.run(100)
    assert web_crawler.visited == {links[0]}
    web_crawler = Crawler(links[1])
    web_crawler.run(100)
    assert web_crawler.visited == {links[1]}

@pytest.mark.parametrize("links",[
    ["/",
    "/login/?2", 
    '#hello', 
    '#', 
    ' ',
    ''
    ]
])
def test_valid_query__webpage(links):
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[0])
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[1])
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[2])
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[3])
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[4])
    with pytest.raises(ValueError):
        web_crawler = Crawler(links[5])

