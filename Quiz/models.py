from django.db import models
from ckeditor.fields import RichTextField
from account.models import User, BaseModel

class Test(BaseModel):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    questions_count = models.IntegerField(default=20)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Question(BaseModel):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question = RichTextField()
    options_count = models.IntegerField(default=4)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.question

class AnswerOption(BaseModel):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class UserTest(BaseModel):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in_process', 'In process'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tests')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='users')
    status = models.CharField(choices=STATUS_CHOICES, default="in_process")
    result = models.IntegerField(default=0)
    completed_data = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} -- {self.test.name}"

class UserTestResponse(BaseModel):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_test}--{self.is_correct}"









