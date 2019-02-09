from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
        'num_buch': num_buch,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10 

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author