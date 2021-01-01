from django.db import models

# Create your models here.



class BookInfo(models.Model):
    # id django 会为我们自动创建一个主键
    # name varchar(10)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "bookinfo"
        verbose_name_plural = verbose_name = "书籍信息"
    # 人物


class PeopleInfo(models.Model):
    # id
    # name
    name = models.CharField(max_length=10)
    # gender 性别
    gender = models.BooleanField()
    # book 外键
    # 外键的级联关系
    # 外键相关的知识 先自己回顾,我们在后天会将
    # 外键在数据库中,系统会自动为我们添加一个 _id
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "peopleinfo"
        verbose_name_plural = verbose_name = "人物信息"
