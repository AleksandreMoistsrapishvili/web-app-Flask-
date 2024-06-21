import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    quotes = soup.select('.quote')
    for quote in quotes:
        text = quote.select_one('.text').text.strip()
        author = quote.select_one('.author').text.strip()
        tags = [tag.text.strip() for tag in quote.select('.tag')]
        data.append([text, author, ', '.join(tags)])

    return data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Quote', 'Author', 'Tags'])
        writer.writerows(data)

def main():
    base_url = 'http://quotes.toscrape.com/page/'
    all_data = []

    for page in range(1, 6):
        url = f'{base_url}{page}/'
        print(f'Fetching: {url}')
        page_data = scrape_page(url)
        all_data.extend(page_data)

    save_to_csv(all_data, 'quotes.csv')

if __name__ == '__main__':
    main()
