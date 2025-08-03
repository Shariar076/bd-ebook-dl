from bs4 import BeautifulSoup
import requests
import os
from time import sleep
html_start ="""<!DOCTYPE html>
<html>
<body>
"""
html_end = """
</body>
</html>
"""

book_file = open(f"দুর্গেশনন্দিনী.html", 'w')

book_file.write(html_start)


def get_page_soup(url):
    page_response = requests.get(url).content
    return BeautifulSoup(page_response, 'html.parser')


def download_chapters(book_title, chap_list):
    for chap_title, chap_addr in chap_list:
        print(chap_title)
        book_file.write(f"<h2>{chap_title}</h2>")
        chap_soup = get_page_soup(chap_addr).find('div', {'class': 'entry-content'})
        while chap_soup is None:
            print("Couldn't get Chapter")
            sleep(30)
            print("Trying again")
            chap_soup = get_page_soup(chap_addr).find('div', {'class': 'entry-content'})
        # chap_soup.button.decompose()
        book_file.write(str(chap_soup))
        # with open(f'{book_title}/{chap_title}.xml', 'w') as soup_file:
        #     soup_file.write(str(chap_soup))


def download_book(book_addr, book_title):
    book_addr_loc = book_addr
    book_file.write(f"<h1>{book_title}</h1>")
    chap_list = []
    while True:
        book_soup = get_page_soup(book_addr_loc)
        chap_list = chap_list + [[article.get('aria-label'), article.find('a', href=True).get('href')] for article in
                                 book_soup.find_all('article')]

        next = book_soup.find("li", class_="pagination-next")
        if next is not None:
            book_addr_loc = next.find("a", class_="pagination-link button button-small", href=True).get("href")
        else:
            break
    print(len(chap_list))
    download_chapters(book_title, chap_list)


#
# page_source = 'https://www.ebanglalibrary.com/category/%e0%a6%ac%e0%a6%99%e0%a7%8d%e0%a6%95%e0%a6%bf%e0%a6%ae%e0%a6%9a%e0%a6%a8%e0%a7%8d%e0%a6%a6%e0%a7%8d%e0%a6%b0-%e0%a6%9a%e0%a6%9f%e0%a7%8d%e0%a6%9f%e0%a7%8b%e0%a6%aa%e0%a6%be%e0%a6%a7%e0%a7%8d%e0%a6%af/%e0%a6%89%e0%a6%aa%e0%a6%a8%e0%a7%8d%e0%a6%af%e0%a6%be%e0%a6%b8-%e0%a6%ac%e0%a6%99%e0%a7%8d%e0%a6%95%e0%a6%bf%e0%a6%ae/'
# soup = get_page_soup(page_source)
#
# with open('soup.txt', 'w') as soup_file:
#     soup_file.write(str(soup))
#
# book_addr_list = [[item.get('href'), item.getText()] for item in soup.find('ol').find_all("a", href =True)]
# for book_addr, book_title in book_addr_list:
#     print(book_title)
#     download_book(book_addr, book_title)
book_addr = 'https://www.ebanglalibrary.com/category/%e0%a6%ac%e0%a6%99%e0%a7%8d%e0%a6%95%e0%a6%bf%e0%a6%ae%e0%a6%9a%e0%a6%a8%e0%a7%8d%e0%a6%a6%e0%a7%8d%e0%a6%b0-%e0%a6%9a%e0%a6%9f%e0%a7%8d%e0%a6%9f%e0%a7%8b%e0%a6%aa%e0%a6%be%e0%a6%a7%e0%a7%8d%e0%a6%af/%e0%a6%89%e0%a6%aa%e0%a6%a8%e0%a7%8d%e0%a6%af%e0%a6%be%e0%a6%b8-%e0%a6%ac%e0%a6%99%e0%a7%8d%e0%a6%95%e0%a6%bf%e0%a6%ae/%e0%a6%a6%e0%a7%81%e0%a6%b0%e0%a7%8d%e0%a6%97%e0%a7%87%e0%a6%b6%e0%a6%a8%e0%a6%a8%e0%a7%8d%e0%a6%a6%e0%a6%bf%e0%a6%a8%e0%a7%80/'
book_title = 'দুর্গেশনন্দিনী'
download_book(book_addr, book_title)
book_file.write(html_end)
book_file.close()
