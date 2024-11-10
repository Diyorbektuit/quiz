from django.urls import path
from Quiz import views


urlpatterns = [
    path('teacher/tests/create/', views.TestCreateView.as_view()),
    path('tests/', views.TestsListView.as_view()),
    path('tests/<int:pk>/', views.TestDetailView.as_view()),
    path('teacher/tests/<int:pk>/update/', views.TestUpdateView.as_view()),
    path('teacher/tests/<int:pk>/delete/', views.TestDeleteView.as_view()),
    path('teacher/questions/create/', views.QuestionCreateView.as_view()),
    path('questions/<int:pk>/', views.QuestionsDetailView.as_view()),
    path('teacher/questions/<int:pk>/update/', views.QuestionUpdateView.as_view()),
    path('teacher/questions/<int:pk>/delete/', views.QuestionDeleteView.as_view()),
    path('teacher/answer_options/create/', views.AnswerOptionCreateView.as_view()),
    path('teacher/answer_options/<int:pk>/delete/', views.AnswerOptionDeleteView.as_view()),
    path('teacher/answer_options/<int:pk>/update/', views.AnswerOptionUpdateView.as_view()),
    path('user_tests/create/', views.UserTestCreateView.as_view()),
    path('user_tests/', views.UserTestListView.as_view()),
    path('user_tests/<int:pk/', views.UserTestsDetailView.as_view()),
    path('user_test/response/create/', views.UserTestResponseCreate.as_view()),
    path('user_test/response/<int:pk>/', views.UserTestResponseUpdate.as_view())

]