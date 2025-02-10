import requests
from bs4 import BeautifulSoup

url = 'https://spdx.org/licenses/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
licenses = {}
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns) >= 2:
        full_name = columns[0].get_text(strip=True).replace('\"', '')
        identifier = columns[1].get_text(strip=True).replace('\"', '')
        if full_name and identifier:
            licenses[full_name] = identifier
max_key_length = max(len(key) for key in licenses.keys())
for key, value in licenses.items():
    print(f'"{key}"{" " * (max_key_length - len(key))} : "{value}",')
