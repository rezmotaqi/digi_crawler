import re
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
import grequests
import requests
from requests import Response
from mongo import products_collection, product_history_collection

base_url = 'https://www.digikala.com'


def get_links() -> list:
    """
    return list of links for 36 most viewed smart phones in first page
    """
    res = requests.get('https://www.digikala.com/search/category-mobile-phone/')
    soup = BeautifulSoup(res.text, 'lxml')
    ul = soup.find("ul", attrs={"class": "c-listing__items js-plp-products-list"})
    a_tags = ul.find_all('a', class_="c-product-box__img c-promotion-box__image js-url js-product-item js-product-url")
    links = []
    for a in a_tags:
        links.append(a.attrs['href'])
    return links


def get_product_page(link: str) -> Response:
    res = requests.get(f'{base_url}' + f'{link}')
    return res


def parse_product_page(res: Response) -> dict:
    soup = BeautifulSoup(res.text, 'lxml')
    product_name = soup.find('div', class_='c-product__title-container').find('h1').text.replace('\n', '').strip()
    final_price = soup.find('div', class_='c-product__seller-price-pure js-price-value').text.replace('\n',
                                                                                                      '').strip()
    before_discount = soup.find('div', class_='c-product__seller-price-info') \
        .find('div', class_='c-product__seller-price-prev js-rrp-price')
    if before_discount is not None:
        before_discount = before_discount.text.replace('\n', '').strip()

    image_link = soup.find('div', class_='c-gallery__img').img.attrs['data-src']

    pid = re.search('^.*/dkp-(\d+)/.*$', res.url)
    product_id = pid.group(1)
    rating_res = requests.get(f'{base_url}' + '/ajax/product/comments/' + product_id + '/')
    rating_soup = BeautifulSoup(rating_res.text, 'lxml')
    ratings_ul = rating_soup.find('ul', class_="c-content-expert__rating")
    ratings = {}
    for li in ratings_ul.find_all('li'):
        key = li.find('div', class_="c-content-expert__rating-title").text
        value = li.find('span', class_="c-rating__overall-word").text
        ratings[key] = value

    data = {
        "product_id": int(product_id),
        "product_link": res.url,
        "product_name": product_name,
        "final_price": final_price,
        "before_discount": before_discount,
        "image_link": image_link,
        "ratings": ratings

    }

    return data


def insert_product(data):
    product = products_collection.find_one(filter={'product_id': data['product_id']})
    if product is not None:
        product_inserted = products_collection.find_one_and_replace(filter={"_id": product['_id']}, replacement={

                "product_id": data['product_id'],
                "product_link": data['product_link'],
                "product_name": data['product_name'],
                "final_price": data['final_price'],
                "before_discount": data['before_discount'],
                "image_link": data['image_link'],
                "ratings": data['ratings']

        })
    else:
        product_inserted = products_collection.insert_one(data)
    return product_inserted


def insert_history(data):
    data['createdAt'] = datetime.now()
    history_inserted = product_history_collection.insert_one(data)
    return history_inserted


def main():
    links = get_links()
    for link in links:
        res = get_product_page(link)
        data = parse_product_page(res)
        product_inserted = insert_product(data)
        history_inserted = insert_history(data)

        print(history_inserted.acknowledged)
        print(product_inserted, 'product inserted')


if __name__ == '__main__':
    main()
