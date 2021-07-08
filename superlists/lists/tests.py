from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_only_save_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the Second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the Second")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list/")
        self.assertTemplateUsed(response, "list.html")
    
    def test_displays_all_items(self):
        Item.objects.create(text="Item One")
        Item.objects.create(text="Item Two")
        response = self.client.get("/lists/the-only-list/")
        self.assertContains(response, "Item One")
        self.assertContains(response, "Item Two")


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual("A new list item", new_item.text)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list")

    
