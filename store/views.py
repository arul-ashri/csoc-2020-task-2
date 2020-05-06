from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

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
    # START YOUR CODE HERE
    
    
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
    book1=Book.objects.get(pk=book_id)
    bookavailable=BookCopy.objects.filter(status__exact=True,book__exact=book1)
    if(bookavailable):
        message="success"
        bookavailable[0].status=False
        bookavailable[0].borrower=request.user
        bookavailable[0].borrow_date= datetime.date.today()
        bookavailable[0].save()
    else:
        message="failure"
    response_data = {
        'message': message,
    }
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = None # get the book id from post data


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
    bookreturn=BookCopy.objects.get(id=book_id)
    if(bookreturn):
        message="success"
        bookreturn.status=True
        bookreturn.borrower=None
        bookreturn.borrow_date=None
        bookreturn.save()
    else:
        message="failure"
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)