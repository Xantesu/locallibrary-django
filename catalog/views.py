from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (Status === a)
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The all() is implied by default.
    num_authors = Author.objects.count()

    # Genres that contain 'fiction'
    num_fiction = Genre.objects.filter(name__contains='french').count()

    # Books that contain 'buch'
    num_buch = Book.objects.filter(title__contains='buch').count()

    # Number of visits from a user, uses sessions
    num_visits = request.session.get('num_visits', 0)

    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
        'num_buch': num_buch,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
   model = BookInstance
   template_name = 'catalog/bookinstance_list_borrowed_user.html'
   paginate_by = 10

   def get_queryset(self):
       return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10 

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author