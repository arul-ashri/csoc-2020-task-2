from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils import datetime_safe

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book1=Book.objects.get(pk=bid)
    num_available=BookCopy.objects.filter(status__exact=True,book__exact=book1).count()
    user_rating=0.0
    

    context = {
        'book': book1, # set this to an instance of the required book
        'num_available': num_available,
        'user_rating': user_rating, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    data=request.GET
    print(len(data))
    if(len(data)>0):
        booklist=Book.objects.filter(title__icontains=data['title'],author__icontains=data['author'],genre__icontains=data['genre'])
    else:
        booklist=Book.objects.all()    
    context = {
        'books': booklist, # set this to the list of required books upon filtering using the GET parameters
                         # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books=BookCopy.objects.filter(borrower__exact=request.user)
    context = {
        'books': books,

    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    


    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    book_id = request.POST.get("bid")
    newbook=Book.objects.get(pk=book_id)
    book=BookCopy.objects.filter(status__exact=True,book__exact=newbook)
    if(book):
        message="success"
        book[0].status=False
        book[0].borrower=request.user
        book[0].borrow_date= datetime_safe.date.today()
        book[0].save()
    else:
        message="failure"
    response_data = {
        'message': message,
    }

    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
   


    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    

    book_id = request.POST.get("bid")
    book=BookCopy.objects.get(id=book_id)
    if(book):
        message="success"
        book.status=True
        book.borrower=None
        book.borrow_date=None
        book.save()
    else:
        message="failure"
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)
@login_required
@csrf_exempt
def bookRatingView(request):
    template_name= template_name = 'store/book_detail.html'
    book_id = request.POST.get("bid")
    rating_value = request.POST.get("rating")
    book1=Book.objects.get(pk=book_id)
    value= BookRating.objects.filter(book__exact=book1,user__exact=request.user)
    if(value.count()>0):
        currentuserRating= BookRating.objects.filter(book__exact=book1,user__exact=request.user).get()
        currentuserRating.ratinguser=rating_value
        currentuserRating.save()
    else:
        BookRating.objects.create(user=request.user,book=book1,ratinguser=rating_value)
    userRating= BookRating.objects.filter(book__exact=book1)
    length=len(userRating)
    avg_rating=0
    for each in userRating:
        avg_rating+=each.ratinguser/length
    book1.rating=avg_rating
    book1.save()
    message="success"
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)