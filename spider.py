import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
import backoff
import logging
from utils import DOWNLOADED_FILE, USER_AGENTS, PAGE_URL, LOG_FILE_NAME, PrometheusLoggingHandler, Gauge, registry, PUSHGATEWAY_URL, push_to_gateway


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def get_page_data(url, headers):
    """Fetch page data with retries on failure."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response

def decode_html_text(advert):
    """Extract and clean data from the HTML content of each advert item."""
    make, color, year, model = None, None, None, None
    description = advert.find('div', class_='qa-advert-title').text.strip()

    if description:
        words = description.split(' ')
        make = words[0]
        color = words[-1]
        year = words[-2]
        model = ' '.join(words[1:-2])

    type_transmission = advert.find_all('div', class_='b-list-advert-base__item-attr')
    type = type_transmission[0].text.strip() if type_transmission else None
    transmission = type_transmission[1].text.strip() if len(type_transmission) > 1 else None

    location = advert.find('span', class_='b-list-advert__region__text')
    location = location.text.strip() if location else 'NA'

    price = advert.find('div', class_='qa-advert-price').text.strip() if advert.find('div', class_='qa-advert-price') else 'NA'

    return {
        'Make': make,
        'Model': model,
        'Year': year,
        'Transmission Type': transmission,
        'Color': color,
        'Type': type,
        'Location': location,
        'Price': price
    }

def main():
    """Fetch car information from multiple pages and save to CSV."""
    car_info = []
    try:
        page_count = 100
        for page in range(1, page_count + 1):
            header = {"User-Agent": random.choice(USER_AGENTS)}
            url = f'{PAGE_URL}?page={page}'

            response = get_page_data(url, headers=header)

            if response.status_code == 200:
                html = BeautifulSoup(response.content, 'lxml')
                advertisements = html.find_all('div', class_='b-list-advert-base__data')

                for advert in advertisements:
                    car_info.append(decode_html_text(advert))

                logging.info(f'Page {page} processed successfully.')
            else:
                logging.warning(f'Request failed with response code: {response.status_code}')

            # Adding a delay to prevent being blocked
            time.sleep(10)

        pd.DataFrame(car_info).to_csv(DOWNLOADED_FILE, mode='w', header=True, index=False)
        logging.info('Data written to file successfully.')

        # Push metrics after processing all pages
        gauge = Gauge(
            'Number of car information retrieved',
            'Number of car information retrieved',
            registry=registry
        )
        gauge.set(len(car_info))
        push_to_gateway(PUSHGATEWAY_URL, job='car_info_job', registry=registry)
        logging.info('Metrics pushed to Prometheus Pushgateway.')

    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    main()
