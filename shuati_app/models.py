from django.db import models
from django.utils import timezone
from .config.config import format_percentage


class BaseModel(models.Model):
    create_time = models.DateTimeField(
        verbose_name="创建时间",
        # auto_now_add=True,
        default=timezone.now,
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name="是否已经删除"
    )

    class Meta:
        abstract = True


# 题目分类
class Tag(BaseModel):
    tag = models.CharField(
        verbose_name="题目标签",
        max_length=50
    )
    nid = models.CharField(max_length=20, verbose_name="编号")

    def __str__(self):
        return self.tag

    def get_question_num(self):
        return Question.objects.filter(
            is_delete=False,
            tag__tag=self.tag
        ).count()

    class Meta:
        db_table = 'shuatiapp_Tag'


# 用户
class User(BaseModel):
    username = models.CharField(
        verbose_name="用户名",
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        verbose_name="邮箱",
        max_length=100,
        unique=True
    )
    detail = models.TextField(
        verbose_name="个人简介",
        blank=True, null=True
    )

    def totalQuestionNum(self):
        return AnswerRecord.objects.filter(
            is_delete=False,
            user=self
        ).count()

    def totalCorrectPercentage(self):
        try:
            return format_percentage(self.totalCorrectNum() / self.totalQuestionNum())
        except:
            return "没有数据"

    def totalCorrectNum(self):
        return AnswerRecord.objects.filter(
            is_delete=False,
            user=self,
            is_correct=True
        ).count()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'shuatiapp_User'


# 提目标
class Question(BaseModel):
    question_id = models.CharField(
        verbose_name="题目编号",
        max_length=20
    )
    # nid = models.CharField(max_length=20, verbose_name="编号")
    question_content = models.TextField(
        verbose_name="题目内容"
    )
    options = models.JSONField(
        verbose_name="题目选项"
                     """
                     {
                         "A":"选项1",
                         "B":"选项2",
                         "C":"选项3",
                         "D":"选项4",
                         "E":"选项5",
                     }
                     """
    )
    correct_answer = models.CharField(
        verbose_name="正确答案",
        max_length=20
    )
    tag = models.ForeignKey(
        to=Tag,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="题目标签",
        related_name="问题的标签"
    )
    answer_detail = models.TextField(
        verbose_name="题目解析",
        default="无"
    )

    def answer_num(self):
        return AnswerRecord.objects.filter(
            is_delete=False,
            question=self
        ).count()

    def correctPercent(self):
        try:
            fenzi = AnswerRecord.objects.filter(
                is_delete=False,
                question=self,
                is_correct=True,
            ).count()
            return format_percentage(fenzi / self.answer_num())
        except:
            return "没有数据"

    def __str__(self):
        return self.question_content

    class Meta:
        db_table = 'shuatiapp_Question'


# 答题记录
class AnswerRecord(BaseModel):
    record_id = models.CharField(
        verbose_name="题目编号",
        max_length=20,
        default=""
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="用户",
        related_name="答题记录的用户"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="题目",
        related_name="答题记录的题目"
    )
    answer = models.CharField(
        max_length=100,
        verbose_name="用户的选项"
    )
    is_correct = models.BooleanField(verbose_name="是否回答正确")
    isInErrorBook = models.BooleanField(
        verbose_name="是否在错题本",
        default=False
    )

    class Meta:
        db_table = 'shuatiapp_AnswerRecord'


class AdminUser(models.Model):
    username = models.CharField(
        verbose_name="管理员用户名",
        max_length=50
    )
    password = models.CharField(
        verbose_name="管理员密码",
        max_length=100
    )
    create_time = models.DateTimeField(
        verbose_name="创建时间",
        auto_now_add=True
    )

    def __str__(self):
        return self.username
