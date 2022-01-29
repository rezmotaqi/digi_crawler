import unittest
from bs4 import BeautifulSoup
import main


class Test(unittest.TestCase):

    def test_get_links(self):
        self.assertNotEqual(0, len(main.get_links()), msg="no links are retrieved")

    def test_link_is_valid(self):
        self.assertIsNotNone(main.get_links()[0])

    def test_get_product_res(self):
        self.assertEqual(main.get_product_page(main.get_links()[0]).status_code, 200)

    def test_product_data_pname(self):
        data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
        self.assertIsNotNone(data['product_name'])

    def test_product_data_prating(self):
        data = main.parse_product_page(main.get_product_page(main.get_links()[0]))
        self.assertIsNotNone(data['ratings'])


if __name__ == '__main__':
    unittest.main()
