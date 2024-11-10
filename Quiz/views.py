from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from Quiz import serializers
from rest_framework import generics
from .models import Test, Question, AnswerOption, UserTestResponse, UserTest
from .permissions import IsTeacher, IsTestOwnerOrSuperuser, IsTeacherOrSuperuser, IsStudent, IsOwner
from .paginations import DefaultPagination
from rest_framework.permissions import IsAuthenticated

class TestCreateView(generics.CreateAPIView):
    serializer_class = serializers.TestSerializerForPost
    queryset = Test.objects.all()
    permission_classes = (IsTeacher, )

class TestUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.TestSerializerForPut
    permission_classes = (IsTestOwnerOrSuperuser, )

    def get_queryset(self):
        user = self.request.user
        if user.role == "superuser":
            return Test.objects.all()
        return self.request.user.tests.filter(active=False)

class TestDeleteView(generics.DestroyAPIView):
    permission_classes = (IsTestOwnerOrSuperuser, )

    def get_queryset(self):
        user = self.request.user
        if user.role == "superuser":
            return Test.objects.all()
        return self.request.user.tests.filter(active=False)

class TestsListView(generics.ListAPIView):
    serializer_class = serializers.TestSerializerForList
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("teacher", "active")
    search_fields = ('name',)
    pagination_class = DefaultPagination


    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return user.tests.all().select_related('teacher')
        elif user.role == "superuser":
            return Test.objects.all().select_related('teacher')
        return Test.objects.filter(active=True)

class TestDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TestSerializerForGet
    queryset = Test.objects.all()
    permission_classes = (IsAuthenticated, )

class QuestionCreateView(generics.CreateAPIView):
    serializer_class = serializers.QuestionSerializerForPost
    queryset = Test.objects.all()
    permission_classes = (IsTeacher, )

class QuestionsDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.QuestionSerializerForGet
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated, )

class QuestionUpdateView(generics.UpdateAPIView):
    permission_classes = (IsTeacherOrSuperuser, )

    def get_serializer_class(self):
        user = self.request.user
        if user.role == "teacher":
            return serializers.QuestionSerializerForPut
        return serializers.QuestionSerializerForPutForAdmin

    def get_queryset(self):
        user = self.request.user
        if user.role == "superuser":
            return Question.objects.all()
        return Question.objects.filter(active=False, test__teacher=user)

class QuestionDeleteView(generics.DestroyAPIView):
    permission_classes = (IsTeacherOrSuperuser, )

    def get_queryset(self):
        user = self.request.user
        if user.role == "superuser":
            return Question.objects.all()
        return Question.objects.filter(active=False, test__teacher=user)


class AnswerOptionCreateView(generics.CreateAPIView):
    serializer_class = serializers.AnswerOptionSerializerForPost
    queryset = AnswerOption.objects.all()
    permission_classes = (IsTeacher, )

    def perform_create(self, serializer):
        question = serializer.validated_data['question']

        if question.options.count() == question.options_count - 1:
            question.active = True
            question.save()

            test = question.test
            if test.questions_count  == test.questions.filter(active=True).count():
                test.active = True
                test.save()

        serializer.save()


class AnswerOptionUpdateView(generics.UpdateAPIView):
    permission_classes = (IsTeacherOrSuperuser, )

    def get_queryset(self):
        user = self.request.user

        if user.role == "superuser":
            return AnswerOption.objects.all()
        return AnswerOption.objects.filter(question__test__teacher=user, question__active=False)

    def get_serializer_class(self):
        user = self.request.user

        if user.role == "superuser":
            return serializers.AnswerOptionSerializerForPutForAdmin
        return serializers.AnswerOptionSerializerForPut


class AnswerOptionDeleteView(generics.DestroyAPIView):
    permission_classes = (IsTeacherOrSuperuser, )

    def get_queryset(self):
        user = self.request.user

        if user.role == "superuser":
            return AnswerOption.objects.all()
        return AnswerOption.objects.filter(question__test__teacher=user, question__active=False)


class UserTestCreateView(generics.CreateAPIView):
    permission_classes = (IsStudent, )
    queryset = UserTest.objects.all()
    serializer_class = serializers.UserTestSerializerForPost

class UserTestListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserTestSerializerForGet
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ("status", "user", "test")
    search_fields = ('test__name', )

    def get_queryset(self):
        user = self.request.user

        if user.role == "superuser":
            return UserTest.objects.all().select_related('user', 'test')
        return user.user_tests.all().select_related('user', 'test')

class UserTestsDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserTestSerializerForGet

    def get_serializer_class(self):
        user = self.request.user
        if user.role == "superuser":
            return serializers.UserTestSerializerForGet
        return serializers.UserTestSerializerForGetStudent

    def get_queryset(self):
        user = self.request.user
        if user.role == "superuser":
            return UserTest.objects.all()
        return user.user_tests.all()

class UserTestFinishView(APIView):
    permission_classes = (IsOwner, )

    def post(self, pk):
        user = self.request.user
        now = timezone.now()
        user_test = UserTest.objects.filter(id=pk, user=user)

        if not user_test.exists():
            raise ValidationError(
                {
                    'msg': "Sizda bunday test mavjud emas"
                }
            )

        user_test = user_test.first()
        correct_answers = user_test.responses.filter(answer_option_is_correct=True)
        correct_answers.update(is_correct=True)
        correct_count = correct_answers.count()
        all_question_count = user_test.test.questions_count

        point = int(correct_count / all_question_count * 100)
        user_test.completed_data = now
        user_test.result = point
        user_test.status = "completed"
        user_test.save()

        return Response(data={
            'all_questions_count': all_question_count,
            'correct_count': correct_count,
            'result': point
        })


class UserTestResponseCreate(generics.CreateAPIView):
    queryset = UserTestResponse.objects.all()
    permission_classes = (IsStudent, )
    serializer_class = serializers.UserTestResponseSerializerForPost

class UserTestResponseUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsStudent, )

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return serializers.UserTestResponseSerializerForGet
        return serializers.UserTestResponseSerializerForPut

    def get_queryset(self):
        user = self.request.user
        return UserTestResponse.objects.filter(user_test__user=user)
















