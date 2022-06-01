from email import contentmanager
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from django.urls import reverse  # Used to generate urls by reversing the URL patterns
from django.db.models.signals import post_save, post_delete
#relation containg all genre of books
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name
##  __str__ method is used to override default string returnd by an object


##relation containing language of books
class Language(models.Model):
    short = models.CharField(max_length = 5, default='en')
    name = models.CharField(max_length=200, default='English',
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.short+ '-' +self.name

class Author(models.Model):
    name=models.CharField(max_length=100)
    # book= models.ManyToManyField(Book)

#book relation that has 2 foreign key author language
#book relation can contain multiple genre so we have used manytomanyfield
class Book(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.CharField(max_length=100, blank=True, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, blank=True, null=True)
    total_copies = models.IntegerField(blank=True, null=True)
    available_copies = models.IntegerField(blank=True, null=True)
    small_pic = models.URLField(blank=True, null=True)
    large_pic = models.URLField(blank=True, null=True)
#return canonical url for an object
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    ##  __str__ method is used to override default string returnd by an object
    def __str__(self):
        return self.title

class EachBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    present = models.BooleanField(null=True , default=True)


def create_user(sender, instance, *args, **kwargs):
    if kwargs['created']:
        s= (instance.roll_no)
        usern=User.objects.create(username=s, password="dummypass")
        usern.set_password('dummypass')
        instance.username=usern
        usern.save()
        print(usern)


class Department(models.Model):
    name=CharField(max_length=30)

class Teacher(models.Model):
    username= models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True, null=True)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    email=models.EmailField(blank=True, null=True)
    pic=models.ImageField(blank=True, upload_to='profile_image')
    def __str__(self):
        return str(self.roll_no)
#relation containing info about students
#roll_no is used for identifing students uniquely
class Student(models.Model):
    username= models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True, null=True)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=1)
    email=models.EmailField(blank=True, null=True)
    yoj = models.IntegerField(blank=True, null=True)
    pic=models.ImageField(blank=True, upload_to='profile_image')
    def __str__(self):
        return str(self.roll_no)

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])


post_save.connect(create_user, sender=Student)
#relation containing info about Borrowed books
#it has  foriegn key book and student for refrencing book nad student
#roll_no is used for identifing students
#if a book is returned than corresponding tuple is deleted from database
class Transfers(models.Model):
    student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.PROTECT)
    eachbook = models.ForeignKey('EachBook', null=True, blank=True, on_delete=models.PROTECT)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return 'S'+self.student.roll_no+'-B'+str(self.eachbook.id)



class Circulation(models.Model):
    transfer=models.ForeignKey(Transfers, null=True, blank=True, on_delete=models.PROTECT)

def IssueReturn(sender, instance, *args, **kwargs):
    if kwargs['created']:
        Circulation.objects.create(transfer=instance)


# def IssueReturnDelete(sender, instance, *args, **kwargs):
#     c= Circulation.objects.get(student=instance.student, book=instance.book)
#     c.delete()


post_save.connect(IssueReturn, sender=Transfers)
# post_delete.connect(IssueReturnDelete, sender=Transfers)


# class Reviews(models.Model):
#     review=models.CharField(max_length=100,default="none")
#     book=models.ForeignKey('Book',on_delete=models.CASCADE)
#     student = models.ForeignKey('Student', on_delete=models.CASCADE)
#     CHOICES = (
#         ('0', '0'),
#         ('.5', '.5'),
#         ('1', '1'),
#         ('1.5', '1.5'),
#         ('2', '2'),
#         ('2.5', '2.5'),
#         ('3', '3'),
#         ('3.5', '3.5'),
#         ('4', '4'),
#         ('4.5', '4.5'),
#         ('5', '5'),
#     )

#     rating=models.CharField(max_length=3, choices=CHOICES, default='2')

class posts(models.Model):
    student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.PROTECT)
    date = models.DateTimeField()
    content = models.CharField(max_length= 100)
    link = models.URLField(blank=True, null=True)
    link_label = models.CharField(max_length=30)

