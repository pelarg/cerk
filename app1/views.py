from django.shortcuts import render
from .models import Item

from django.shortcuts import render, redirect
from .models import Item


def item_listt(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            Item.objects.create(title=title, text=text)
            return redirect('item_listt')
    search_query = request.GET.get('search', '')
    items=Item.objects.filter(title__icontains=search_query)

    return render(request, 'app1/item_listt.html', {'items': items, 'search_query': search_query})

def item_detail(request):
    return render(request, 'app1/item_detail.html')
