from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_home_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        test_list = List()
        test_list.save()
        
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = test_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the Second"
        second_item.list = test_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, test_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, test_list)
        self.assertEqual(second_saved_item.text, "Item the Second")
        self.assertEqual(second_saved_item.list, test_list)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        test_list = List.objects.create()
        Item.objects.create(text="Item One", list=test_list)
        Item.objects.create(text="Item Two", list=test_list)
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
        self.assertRedirects(response, "/lists/the-only-list/")
