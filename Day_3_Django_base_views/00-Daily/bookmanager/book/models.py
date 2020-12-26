from django.db import models


# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=20)
    pub_date = models.DateField(null=True)
    readcount = models.IntegerField(default=1)
    commentcount = models.IntegerField(default=1)
    is_delete = models.IntegerField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bookinfo'  # 数据库表面可以修改
        verbose_name_plural = verbose_name = '图书信息'


class PeopleInfo(models.Model):
    name = models.CharField(max_length=20)
    GENDER_CHOICE = (
        (0, 'boy'),
        (1, 'girl')
    )
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=0)
    description = models.CharField(max_length=128, null=True)
    is_delete = models.BooleanField(default=False)
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'PeopleInfo'
        verbose_name_plural = verbose_name = '任务信息'
