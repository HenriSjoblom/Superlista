from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List

User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    shared_lists = List.get_shared_lists(owner)
    return render(request, 'my_lists.html', {'owner': owner, 'shared_lists': shared_lists})


def share_list(request, list_id):
    email = request.POST['sharee']
    list_ = List.objects.get(id=list_id)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(email=email)
    list_.share_list(user)
    return redirect(list_)