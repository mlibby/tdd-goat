from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")

def new_list(request):
    new_item_text = request.POST.get("item_text", "")
    new_list = List.objects.create()
    Item.objects.create(text=new_item_text, list=new_list)
    return redirect("/lists/the-only-list/")

def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
