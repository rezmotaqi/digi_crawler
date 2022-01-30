import asyncio
import random
import unittest
from bs4 import BeautifulSoup
import main
from aiohttp import ClientSession
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def gen_random_page_number():
    return random.randint(0, 36)


# async driver
async def get_pages():
    async with ClientSession() as session:
        res = await asyncio.gather(*(main.get_product_page(link, session) for link in main.get_links()))
        return res


async def parse(response):
    data = await main.parse_product_page(*response)
    return data


def get_data():
    page_number = gen_random_page_number()
    res = asyncio.run(get_pages())[page_number]
    data = asyncio.run(parse(response=res))

    return data


class Test(unittest.TestCase):

    def test_get_links(self):
        self.assertNotEqual(0, len(main.get_links()), msg="no links are retrieved")

    def test_link_is_valid(self):
        self.assertIsNotNone(main.get_links()[0])

    def test_get_product_res(self):
        page = gen_random_page_number()
        self.assertEqual(asyncio.run(get_pages())[page][0].status, 200)

    def test_product_data_pname(self):
        data = get_data()
        self.assertIsNotNone(data['product_name'])

    def test_product_data_rating(self):
        data = get_data()
        self.assertIsNotNone(data['ratings'])

    def test_insert_history(self):
        data = get_data()
        self.assertEqual(main.insert_history(data).acknowledged, True)

    def test_insert_product(self):
        data = get_data()
        self.assertIsNotNone(main.insert_product(data), True)


if __name__ == '__main__':
    unittest.main()

    # def test_get_links(self):
    #     self.assertNotEqual(0, len(main.get_links()), msg="no links are retrieved")
    #
    # def test_link_is_valid(self):
    #     self.assertIsNotNone(main.get_links()[0])
    #
    # def test_get_product_res(self):
    #     self.assertEqual(main.get_product_page(main.get_links()[0]).status_code, 200)
    #
    # def test_product_data_pname(self):
    #     data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
    #     self.assertIsNotNone(data['product_name'])
    #
    # def test_product_data_prating(self):
    #     data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
    #     self.assertIsNotNone(data['ratings'])
    #
    # def test_insert_history(self):
    #     data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
    #     self.assertEqual(main.insert_history(data).acknowledged, True)
    #
    # def test_insert_product(self):
    #     data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
    #     self.assertIsNotNone(main.insert_product(data), True)
