from django.db import models


# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=10)
    pub_date = models.DateField(null=True)
    readcount = models.IntegerField(default=0)
    commentcount = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookinfo'
        verbose_name = '图书信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)
    GENDER_CHOICE = (
        (0, 'boy'),
        (1, 'girl'),
    )
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=0)
    description = models.CharField(max_length=10)
    is_delete = models.BooleanField(default=False)
    book_id = models.ForeignKey(BookInfo,on_delete=models.CASCADE)
    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
