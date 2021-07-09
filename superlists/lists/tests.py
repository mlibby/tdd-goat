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
        test_list = List.objects.create()
        response = self.client.get(f"/lists/{test_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        test_list = List.objects.create()
        Item.objects.create(text="Item One", list=test_list)
        Item.objects.create(text="Item Two", list=test_list)
        other_list = List.objects.create()
        Item.objects.create(text="Other Item One", list=other_list)
        Item.objects.create(text="Other Item Two", list=other_list)

        response = self.client.get(f"/lists/{test_list.id}/")

        self.assertContains(response, "Item One")
        self.assertContains(response, "Item Two")
        self.assertNotContains(response, "Other Item One")
        self.assertNotContains(response, "Other Item Two")

    def test_passes_correct_list_to_template(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    def test_can_save_POST_request_to_existing_list(self):
        response = self.client.post(
            f"/lists/new",
            data={"item_text": "A new list item"},
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            f"/lists/new",
            data={"item_text": "A new list item"},
        )
        new_list = List.objects.first()

        self.assertRedirects(response, f"/lists/{new_list.id}/")


class NewItemTest(TestCase):
    def test_can_save_POST_request_to_existing_list(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
