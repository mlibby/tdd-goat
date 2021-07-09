from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 3


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assertRowTextInListTable(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_start_list_retrieve_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)
        h1_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", h1_text)

        new_item_label = self.browser.find_element_by_id("new_item_label")
        self.assertEqual(new_item_label.text, "Enter a to-do item")
        self.assertEqual(new_item_label.get_attribute("for"), "new_item_input")

        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Buy peacock feathers")
        new_item_input.send_keys(Keys.ENTER)

        self.assertRowTextInListTable("1: Buy peacock feathers")

        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Use peacock feathers to make a fly")
        new_item_input.send_keys(Keys.ENTER)

        self.assertRowTextInListTable("1: Buy peacock feathers")
        self.assertRowTextInListTable("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists(self):
        self.browser.get(self.live_server_url)
        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Buy peacock feathers")
        new_item_input.send_keys(Keys.ENTER)
        self.assertRowTextInListTable("1: Buy peacock feathers")

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # new user visits
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # new visitor creates new list
        new_item_input = self.browser.find_element_by_id("new_item_input")
        new_item_input.send_keys("Buy milk")
        new_item_input.send_keys(Keys.ENTER)
        self.assertRowTextInListTable("1: Buy milk")

        # new visitor has own list
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
