from email import message
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import*
import json
# from openpyxl import load_workbook
# Python's built-in module for opening and reading URLs
from urllib.request import urlopen
from .models import *
from .forms import *
# .FORMS REFERS TO THE FORMS.PY IN CURRENT DIRECTORY AND * USED FOR IMPORTING EVERYTHING

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

# HOME PAGE
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'catalog/contact.html')

# VIEW THAT WILL RETURN LIST OF ALL BOOKS IN LIBRARY
def BookListView(request):
    book_list = Book.objects.all()
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalog/book_list.html', locals())

@login_required
def student_BookListView(request):
    student=Student.objects.get(roll_no=request.user)
    bor=Circulation.objects.filter(transfer__student=student)
    book_list=[]
    for b in bor:
        book_list.append(b.book)
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalog/book_list.html', locals())

#This view return detail of a particular book
#it also accepts a parameter pk that is the id  i.e. primary_key of book to identify it
#get_object_404 if object is not found then return 404 server error
#locals return a dictionary of loacl varibles
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    # reviews=Reviews.objects.filter(book=book).exclude(review="none")
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
            # send a request and get a JSON response
    resp = urlopen(api + book.isbn)
    book_data = json.load(resp)
    print(book_data)
            # create additional variables for easy querying
            
    try:
        summary = book_data["items"][0]["volumeInfo"]['description']
    except:
        summary=NULL
        message='Summary not found.'
        
    try:
        stu = Student.objects.get(roll_no=request.user)
        # rr=Reviews.objects.get(review="none")
    except:
        pass
    return render(request, 'catalog/book_detail.html', locals())



# --------------_++++++++++++++++ ADD 128 RANDOM BOOKS ++++++++++++++++++_----------------------

# @login_required
# def addrandombooks(request):
#     if not request.user.is_superuser:
#         return redirect('index')
# form = BookForm()
    # # if request.method == 'POST':

    #     # ==================== ENTRY FOR TEST TIMEEEEE ===========================
    # workbook = load_workbook(filename="Book_ISBN.xlsx")
    # sheet = workbook.active
    # b=Book()
    # for i in range(1,128):
    #     isbn = str(sheet.cell(row=i, column=1).value)
    #     tc= 10
    #     api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    #     # send a request and get a JSON response
    #     resp = urlopen(api + isbn)
    #     book_data = json.load(resp)
    #     # create additional variables for easy querying
            
    #     try:
    #         volume_info = book_data["items"][0]["volumeInfo"]
    #     except:
    #         volume_info=NULL
    #         message='Book not found.'
    #         pass

    #     try:
    #         title = volume_info['title']
    #     except:
    #         title=NULL
    #         pass
    #     author=''
    #     try:
    #         authors = volume_info["authors"]
    #         # practice with conditional expressions!
    #         for i in authors:
    #             author = author + ', ' + str(i)
    #     except:
    #         author=NULL
    #         pass

    #     try:
    #         small_pic = volume_info['imageLinks']['smallThumbnail']
    #     except:
    #         small_pic = 'https://www.vhv.rs/dpng/d/507-5071204_star-cute-clipart-clipart-royalty-free-clipart-cartoon.png'
    #         msg='No Image'

    #     try:
    #         large_pic = volume_info['imageLinks']['thumbnail']
    #     except:
    #         large_pic = 'https://www.vhv.rs/dpng/d/507-5071204_star-cute-clipart-clipart-royalty-free-clipart-cartoon.png'
    #         msg='No Image'


    #     if volume_info is not NULL:
    #         b=Book.objects.create(title = title ,author=author, isbn=isbn, small_pic = small_pic, large_pic=large_pic, total_copies=tc)

    #         print(f"\nTitle: {volume_info['title']}")
    #         print(f"Author: {author}")
    #         # print(f"Page Count: {volume_info['pageCount']}")
    #         # print(f"Publication Date: {volume_info['publishedDate']}")
    #         print("\n***\n")
    #         b.save()

    #         for i in range(tc):
    #             e=EachBook.objects.create(book=b)
    #             e.save()
    # return redirect(index)

@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            tc= form.cleaned_data['total_copies']
            api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
            # send a request and get a JSON response
            resp = urlopen(api + isbn)
            book_data = json.load(resp)
            # create additional variables for easy querying
            
            try:
                volume_info = book_data["items"][0]["volumeInfo"]
            except:
                volume_info=NULL
                message='Book not found.'
                pass

            try:
                title = volume_info['title']
            except:
                title=NULL
                pass

            try:
                authors = volume_info["authors"]
                # practice with conditional expressions!
                for i in authors:
                    author = author + str(i) + ','
            except:
                author=NULL

            try:
                small_pic = volume_info['imageLinks']['smallThumbnail']
            except:
                small_pic = NULL

            try:
                large_pic = volume_info['imageLinks']['thumbnail']
            except:
                large_pic = NULL


            if volume_info is not NULL:
                b=Book.objects.create(title = title ,author=author, isbn=isbn, small_pic = small_pic, large_pic=large_pic, total_copies=tc)

                print(f"\nTitle: {volume_info['title']}")
                print(f"Author: {author}")
                print(f"Page Count: {volume_info['pageCount']}")
                print(f"Publication Date: {volume_info['publishedDate']}")
                print("\n***\n")
                b.save()

                for i in range(tc):
                    e=EachBook.objects.create(book=b)
                    e.save()
                return redirect(index)

    return render(request, 'catalog/form.html', locals())


@login_required
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('index')



@login_required
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu=Student.objects.get(roll_no=request.user)
    s = get_object_or_404(Student, roll_no=str(request.user))
    if s.total_books_due < 10:
        message = "You can issue the book from library."
    else:
        message = "you have exceeded limit."
    return render(request, 'catalog/result.html', locals())


@login_required
def StudentCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s=form.cleaned_data['roll_no']
            form.save()
            print(s)
            u=User.objects.get(username=s)
            s=Student.objects.get(roll_no=s)
            u.email=s.email
            u.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def StudentUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Student.objects.get(id=pk)
    form = StudentForm(instance=obj)
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def StudentDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Student, pk=pk)
    obj.delete()
    return redirect('index')

@login_required
def StudentList(request):
    students = Student.objects.all()
    return render(request, 'catalog/student_list.html', locals())

@login_required
def StudentDetail(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    student = get_object_or_404(Student, id=pk)
    books=Transfers.objects.filter(student=student)
    return render(request, 'catalog/student_detail.html', locals())


@login_required
def transfers(request):
    if not request.user.is_superuser:
        return redirect('/')
    return render(request,'catalog/transfer.html' )
    
@login_required
def issue(request):
    if not request.user.is_superuser:
        return redirect('/')
    
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TransferForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            bid = form.cleaned_data['bid']
            sid = form.cleaned_data['sid']

            b=EachBook.objects.get(id=bid)
            s=Student.objects.get(roll_no=sid)

            Bcopy= b.book.available_copies
            Scopy= s.total_books_due

            if(Bcopy>0 and Scopy<7):
                b.book.available_copies=Bcopy-1
                s.total_books_due=Scopy+1


                t=Transfers.objects.create(eachbook=b, student=s, issue_date=datetime.utcnow())
                # Circulation.objects.create(transfer=t)
                b.save()
                print(b)
                print(s)
                s.save()
                t.save()
            # redirect to a new URL:
            return redirect('/transfer/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TransferForm()

    return render(request, 'catalog/issue.html', {'form': form})

@login_required
def ret(request):
    if not request.user.is_superuser:
        return redirect('/')
    
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TransferForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            bid = form.cleaned_data['bid']
            sid = form.cleaned_data['sid']

            b=EachBook.objects.get(id=bid)
            s=Student.objects.get(roll_no=sid)

            Bcopy= b.book.available_copies
            Scopy= s.total_books_due

            if(Bcopy>0 and Scopy>0):
                b.book.available_copies=Bcopy+1
                s.total_books_due=Scopy-1


                t=Transfers.objects.filter(eachbook=b, student=s).last()
                print(t)
                t.return_date= datetime.utcnow()
                c=Circulation.objects.filter(transfer=t).last()
                print(c)
                c.delete()
                b.save()
                print(b)
                print(s)
                s.save()
                t.save()
            # redirect to a new URL:
            return redirect('/transfer/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TransferForm()

    return render(request, 'catalog/issue.html', {'form': form})


import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'catalog/book_list.html',locals() )
def search_student(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['roll_no','name','email'])

        students= Student.objects.filter(entry_query)

    return render(request,'catalog/student_list.html',locals())



# ========================== BOOK RATINGS ==============================================

# ---------------------- RATING UPDATE-------------
# @login_required
# def RatingUpdate(request, pk):
#     obj =Reviews.objects.get(id=pk)
#     form = RatingForm(instance=obj)
#     if request.method == 'POST':
#         form = RatingForm(data=request.POST, instance=obj)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.save()
#             return redirect('book-detail',pk=obj.book.id)
#     return render(request, 'catalog/form.html', locals())


# ---------------------- RATING DELETE -------------
# @login_required
# def RatingDelete(request, pk):
#     obj = get_object_or_404(Reviews, pk=pk)
#     st=Student.objects.get(roll_no=request.user)
#     if not st==obj.student:
#         return redirect('index')
#     pk = obj.book.id
#     obj.delete()
#     return redirect('book_detail',pk)
