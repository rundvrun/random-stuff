import requests
from bs4 import BeautifulSoup
import concurrent.futures
from functools import reduce

def get_page(i):
    print(f'Getting page {i}')
    response = requests.get(f'https://kndict.com/truyen-chem/truyen-chem-tu-sang-tac/page/{i}', cookies={}, headers={})
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    a_tags = soup.select('a[href^="/truyen-chem/"].read-link')
    print(f'Getting page {i} Done')
    return list(set(map(lambda a: 'https://kndict.com' + a.attrs['href'], a_tags)))

def get_html(page):
    print(f'Getting HTML {page}')
    response = requests.get(page, cookies={}, headers={})
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    print(f'Getting HTML {page} Done')
    return str(soup.select_one('#story-content'))

def save_page(i):
    print(f'Process page-{i}')
    with concurrent.futures.ThreadPoolExecutor() as executor: results = list(executor.map(get_html, get_page(i)))
    with open(f'truyen-chem-{i}.xhtml', 'w', encoding='utf-8') as file: file.write(reduce(lambda s, r: s.replace(*r), ['\n'.join(results), ('<span', '<b'), ('span>', 'b>'), ('\xa0', ''), ('./</div>', '.</div><br/>')]))
    print(f'Process page-{i} Done')
    return i


with concurrent.futures.ThreadPoolExecutor() as executor: results = list(executor.map(save_page, range(1, 86)))
print(results)
