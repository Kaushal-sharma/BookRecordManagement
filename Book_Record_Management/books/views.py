from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from books.forms import addbookforms
from books.models import bookTable
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_login(request):
    data = {}
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('http://localhost:8000/books/dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'login_form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/books/login')

#@login_required(login_url='http://localhost:8000/books/login')
def dashboard(request):
    total_book = bookTable.objects.all().count()
    #book = bookTable.objects.values('title').annotate(total=Count('title'))
    #book = bookTable.objects.raw( 'SELECT id, title, COUNT(title) AS total FROM books_booktable GROUP BY title ')
    book = bookTable.objects.raw(' SELECT "books_bookTable"."id", "books_booktable"."title", COUNT("books_booktable"."title") AS "total" FROM "books_booktable" GROUP BY "books_booktable"."title"')
    print("Count:::", book.query)
    dict = {'book':book, 'total_book':total_book}
    res = render(request, 'books/dashboard.html', dict)
    return res

#@login_required(login_url='http://localhost:8000/books/login')
def addTable(request):
    take_form = addbookforms()
    dict = {'showform':take_form}
    if request.method == 'POST':
        form_data = addbookforms(request.POST)
        book = bookTable()
        book.title = form_data.data['title'].title()
        book.author = form_data.data['author'].title()
        book.publisher = form_data.data['publisher']
        book.price = form_data.data['price']
        messages.success(request, 'Successfully added book !')
        book.save()
    res = render(request, 'books/addbook.html', dict)
    return res

#@login_required(login_url='http://localhost:8000/books/login')
def showResult(request):
    table_data = bookTable.objects.all()
    #table_data = bookTable.objects.raw('select * from books_bookTable where price > 450 order by price')
    #table_data = bookTable.objects.raw('select id , min(price) from books_bookTable')
    print("Record::::", table_data)
    dict = {'result':table_data}
    res = render(request, 'books/viewbook.html', dict)
    return res

#@login_required(login_url='http://localhost:8000/books/login')
def editform(request):
    book = bookTable.objects.get(id=request.GET['bookid'])
    fields = {'title':book.title, 'author':book.author, 'publisher':book.publisher, 'price':book.price}
    form = addbookforms(initial=fields)
    res = render(request, 'books/editbook.html', {'form':form, 'book':book})
    return res

#@login_required(login_url='http://localhost:8000/books/login')
def update(request):
    if request.method == 'POST':
        form = addbookforms(request.POST)
        book = bookTable()
        book.id = request.POST['bookid']
        book.title = form.data['title']
        book.author = form.data['author']
        book.publisher = form.data['publisher']
        book.price = form.data['price']
        book.save()
        res = HttpResponseRedirect('http://localhost:8000/books/showresult/')
        return res

#@login_required(login_url='http://localhost:8000/books/login')
def delete(request):
    getid = request.GET['id']
    delete_one_row = bookTable.objects.filter(id=getid)
    print("Delete Query::", delete_one_row.query)
    delete_one_row.delete()
    print("Return :: ", delete_one_row)
    return HttpResponseRedirect('http://localhost:8000/books/showresult/')
