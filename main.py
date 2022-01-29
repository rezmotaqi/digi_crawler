import re

from bs4 import BeautifulSoup
import requests

base_url = 'https://www.digikala.com'


def get_links():
    res = requests.get('https://www.digikala.com/search/category-mobile-phone/')
    soup = BeautifulSoup(res.text, 'lxml')
    ul = soup.find("ul", attrs={"class": "c-listing__items js-plp-products-list"})
    a_tags = ul.find_all('a', class_="c-product-box__img c-promotion-box__image js-url js-product-item js-product-url")
    links = []
    for a in a_tags:
        links.append(a.attrs['href'])

    return links


async def get_product_info(product_link):
    """
    gets product link and returns object of dict type containing data for given link
    """
    res = requests.get(f'{base_url}' + f'{product_link}')
    soup = BeautifulSoup(res.text, 'lxml')
    product_name = soup.find('div', class_='c-product__title-container').find('h1').text.replace('\n', '').strip()
    final_price = soup.find('div', class_='c-product__seller-price-pure js-price-value').text.replace('\n', '').strip()

    discount_price = soup.find('div', class_='c-product__seller-price-info') \
        .find('div', class_='c-product__seller-price-prev js-rrp-price')
    if discount_price is not None:
        discount_price = discount_price.text.replace('\n', '').strip()

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
        "product_link": product_link,
        "product_name": product_name,
        "price": final_price,
        "discount_price": discount_price,
        "image_link": image_link,
        "ratings": ratings

    }
    return data



def main():
    for product_link in get_links():
        data = get_product_info(product_link)
        print(data)


if __name__ == '__main__':
    main()

