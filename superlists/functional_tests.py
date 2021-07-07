from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assertRowTextInListTable(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_start_list_retrieve_later(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("To-Do", self.browser.title)
        h1_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", h1_text)

        new_item_label = self.browser.find_element_by_id("new_item_label")
        self.assertEqual(new_item_label.text, "Enter a to-do item")
        self.assertEqual(new_item_label.get_attribute("for"), "new_item_input")

        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Buy peacock feathers")
        new_item_input.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assertRowTextInListTable("1: Buy peacock feathers")

        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Use peacock feathers to make a fly")
        new_item_input.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assertRowTextInListTable("1: Buy peacock feathers")
        self.assertRowTextInListTable("2: Use peacock feathers to make a fly")

        self.fail("Add more tests")


if __name__ == "__main__":
    unittest.main()
