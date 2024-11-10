from django.contrib import admin
from .models import Test, Question, AnswerOption

# Register your models here.
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'name', 'questions_count', 'active')
    list_filter = ('teacher',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'question', 'options_count', 'active')
    list_filter = ('test', )

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_text', 'is_correct')
    list_filter = ('question', )

