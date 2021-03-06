import datetime
from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author, Book

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

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed_books'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renewal_librarian.html', context)


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
   model = BookInstance
   template_name = 'catalog/borrowed_books_list.html'
   permission_required = 'catalog.can_mark_returned'

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


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
