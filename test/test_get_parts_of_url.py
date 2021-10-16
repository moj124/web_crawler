import pytest
from ..crawl_website import get_parts_of_url

@pytest.mark.parametrize("links",[
    ["https://www.scrapethissite.com/faq/",
    "https://www.scrapethissite.com/", 
    "https://www.scrapethissite.com/lessons/", 
    "https://www.scrapethissite.com/pages/", 
    "https://www.scrapethissite.com/login/"]
])
def test_url_format(links):
    assert get_parts_of_url(links[0]) == ('scrapethissite.com','https://www.scrapethissite.com','https://www.scrapethissite.com/faq/')
    assert get_parts_of_url(links[1]) == ('scrapethissite.com','https://www.scrapethissite.com','https://www.scrapethissite.com/')
    assert get_parts_of_url(links[2]) == ('scrapethissite.com','https://www.scrapethissite.com','https://www.scrapethissite.com/lessons/')
    assert get_parts_of_url(links[3]) == ('scrapethissite.com','https://www.scrapethissite.com','https://www.scrapethissite.com/pages/')
    assert get_parts_of_url(links[4]) == ('scrapethissite.com','https://www.scrapethissite.com','https://www.scrapethissite.com/login/')

@pytest.mark.parametrize("links",[
    ["/",
    "/login/?2", 
    '#hello', 
    '#', 
    ' ',
    ''
    ]
])
def test_url_endpoints(links):
    assert get_parts_of_url(links[0]) == ('','://','/')
    assert get_parts_of_url(links[1]) == ('','://','/login/')
    assert get_parts_of_url(links[2]) == ('','://','#hello')
    assert get_parts_of_url(links[3]) == ('','://','#')
    assert get_parts_of_url(links[4]) == ('','://',' ')
    assert get_parts_of_url(links[5]) == ('','://','')



