from django.db import models

# Create your models here.



class BookInfo(models.Model):
    # id django 会为我们自动创建一个主键
    # name varchar(10)
    name = models.CharField(max_length=10, verbose_name='admin站点相关不是重点')
    pub_date = models.DateField(null=True)
    readcount = models.IntegerField(default=0)
    commentcount = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "bookinfo"
        verbose_name_plural = verbose_name = "书籍信息"
    # 人物


class PeopleInfo(models.Model):
    GENDER_CHOICE = (
        (0, 'boy'),
        (1, 'girl')
    )
    # (值,说明)
    """
    id
    name 人物名
    gender 性别
    description 描述
    is_delete 是否删除
    book_id 书籍外键
    """
    name = models.CharField(max_length=10)
    # choices 选项 只能从 元组中选取一个
    # choices 的值 我们定义元组
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=0)
    description = models.CharField(max_length=100, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "peopleinfo"
        verbose_name_plural = verbose_name = "人物信息"

    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
