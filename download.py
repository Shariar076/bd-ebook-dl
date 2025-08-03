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
main_out_filename = "মনের মানুষ - সুনীল গঙ্গোপাধ্যায়"

book_file = open(f"{main_out_filename}.html", 'w')

book_file.write(html_start)


def get_page_soup(url):
    HEADER = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; SM-T395) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.83 Safari/537.36'}
    PROXY = {"https": "https//59.110.7.190:1080"}
    try:
        page_response = requests.get(url, 
                                    #  proxies=PROXY, 
                                    #  headers=HEADER
                                    timeout=5
                                    ).content
    except:
        page_response = None
    return BeautifulSoup(page_response, 'html.parser')


def download_chapters(book_title, chap_list):
    for chap_title, chap_addr in chap_list:
        print(chap_title.text)
        book_file.write(f"<h2>{chap_title.text}</h2>")
        chap_soup = None
        while chap_soup is None:

            chap_soup = get_page_soup(chap_addr).find('div', {'class': 'entry-content'}).find_all('p')
            if chap_soup is None:
                print("Couldn't get Chapter")
                sleep(30)
                print("Trying again")
            else:
                print("Done")
                sleep(1)
                break
        # chap_soup.button.decompose()
        book_file.write('\n'.join([f"<p>{par.text}</p>" for par in chap_soup]))
        # with open(f'{book_title}/{chap_title}.xml', 'w') as soup_file:
        #     soup_file.write(str(chap_soup))


def download_book(book_addr, book_title):
    book_addr_loc = book_addr
    book_file.write(f"<h1>{book_title}</h1>")
    chap_list = []
    while True:
        book_soup = get_page_soup(book_addr_loc)
        # chap_list = chap_list + [[article.get('aria-label'), article.find('a', href=True).get('href')] for article in
        #                          book_soup.find_all('article')]
        chap_list = chap_list + [[article.find(class_= 'ld-item-title'), article.find('a', href=True).get('href')] for article in
                                 book_soup.find_all(class_='ld-item-list-item')]

        next = book_soup.find("li", class_="pagination-next")
        if next is not None:
            book_addr_loc = next.find("a", class_="pagination-link button button-small", href=True).get("href")
        else:
            break
    print(len(chap_list))
    # print(chap_list)
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
book_addr = 'https://www.ebanglalibrary.com/books/%E0%A6%AE%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A6%AE%E0%A6%BE%E0%A6%A8%E0%A7%81%E0%A6%B7-%E0%A6%B8%E0%A7%81%E0%A6%A8%E0%A7%80%E0%A6%B2-%E0%A6%97%E0%A6%99%E0%A7%8D%E0%A6%97%E0%A7%8B%E0%A6%AA%E0%A6%BE/'
book_title = 'মনের মানুষ'
download_book(book_addr, book_title)
book_file.write(html_end)
book_file.close()


os.system(f'pandoc -f html -t epub3 -o "{main_out_filename}.epub" "{main_out_filename}.html"')