import requests
from bs4 import BeautifulSoup
import csv

def extract_page_data(soup):
    items = soup.find_all('div', {'class': 'v2-listing-card__info'})
    data = []
    for item in items:
        # item name
        name_tag = item.find('h3', {'class': ['wt-text-caption', 'v2-listing-card__title', 'wt-text-truncate']})
        item_name = name_tag.get_text(strip=True) if name_tag else 'No Title'
        
        # item price
        price_element = item.find('span', {'class': 'currency-value'})
        price = price_element.text.strip() if price_element else 'No price'
        price=round(float(price.replace(',', '')))
                
        # free shipping status
        shipping_element = item.find('span', {'class': 'wt-text-grey wt-text-body-smaller'})
        free_shipping = 'Yes' if shipping_element and 'Free shipping' in shipping_element.text else 'No'
                
        # number of reviews
        review_count_element = item.find('p', {'class': 'wt-text-body-smaller'})
        review_count = review_count_element.text.strip().replace('(', '').replace(')', '')

        if 'k' in review_count:
            # Remove 'k' and add '000' if there's no decimal point
            if '.' not in review_count:
                review_count = review_count.replace('k', '000')
            else:
                # If there's a decimal point, remove it and add '00'
                review_count = review_count.replace('k', '').replace('.', '') + '00'

        review_count = int(review_count) if review_count.isdigit() else 'No reviews'
        
        data.append([item_name, price, free_shipping, review_count])
    return data

# Main function to scrape data
def scrape_etsy(url, pages):
    all_data = []
    for page in range(1, pages + 1):
        print(f'Scraping page {page}...')
        response = requests.get(url + f'&page={page}')
        soup = BeautifulSoup(response.content, 'html.parser')
        page_data = extract_page_data(soup)
        all_data.extend(page_data)
    return all_data

# URL of the Etsy category to scrape
url = 'https://www.etsy.com/search?q=dog%20house&ref=search_bar'

#number of pages to scrape
pages_to_scrape = 300

# Scraping data
data = scrape_etsy(url, pages_to_scrape)

# Save data to CSV
with open('C:\미국SWP/etsy_dog.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Item Title', 'Item Price', 'Free Shipping', 'Total reviews'])
    writer.writerows(data)
print('Scraping completed')