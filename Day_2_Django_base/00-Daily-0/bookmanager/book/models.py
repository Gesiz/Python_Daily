from django.db import models


# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)

    gender = models.BooleanField()

    book_id = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
