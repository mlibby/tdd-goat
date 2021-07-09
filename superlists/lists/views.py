from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def new_list(request):
    new_item_text = request.POST.get("item_text", "")
    new_list = List.objects.create()
    Item.objects.create(text=new_item_text, list=new_list)
    return redirect(f"/lists/{new_list.id}/")


def view_list(request, list_id):
    vlist = List.objects.get(id=list_id)
    items = Item.objects.filter(list=vlist)
    return render(request, "list.html", {"list": vlist})


def add_item(request, list_id):
    vlist = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=vlist)
    return redirect(f"/lists/{vlist.id}/")
