from rest_framework import serializers
from .models import Test, Question, AnswerOption, UserTest, UserTestResponse
from account.views import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile_image'
        )

class TestQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question'
        )

class TestSerializerForGet(serializers.ModelSerializer):
    teacher_data = UserSerializer(source='teacher')
    questions_data = TestQuestionsSerializer(source='questions', many=True)
    class Meta:
        model = Test
        fields = (
            'id',
            'name',
            'teacher_data',
            'questions_data',
            'active'
        )

class TestSerializerForList(serializers.ModelSerializer):
    teacher_data = UserSerializer(source='teacher')
    class Meta:
        model = Test
        fields = (
            'id',
            'name',
            'questions_count',
            'teacher_data'
        )

class TestSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'name',
        )


class TestSerializerForPost(serializers.ModelSerializer):
    teacher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Test
        fields = (
            'name',
            'teacher'
        )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name

        }

    def validate(self, attrs):
        name = attrs['name']

        if len(name) > 100:
            raise serializers.ValidationError(
                {
                    'msg': "Testni nomi 100ta belgidan oshmasligi kerak"
                }
            )

        return attrs

class AnswerOptionSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = (
            'id',
            'option_text',
        )

class QuestionSerializerForGet(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializerForGet(source='options', many=True)
    class Meta:
        model = Question
        fields = (
            'id',
            'question',
            'answer_options',
            'options_count',
            'active',
        )

class QuestionSerializerForPutForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'question',
            'options_count',
            'active',
        )

class QuestionSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'question',
            'options_count',
        )


class QuestionSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'test',
            'question',
            'options_count'
        )

    def validate(self, attrs):
        test = attrs.get('test')
        questions_count = test.questions.all().count()

        if questions_count >= test.questions_count:
            raise serializers.ValidationError(
                {
                    'msg': f"Bu testning maksimal savollari soni {test.questions_count} ta"
                }
            )
        return attrs

    def to_representation(self, instance):
        test_data = {
            'id': instance.test.id,
            'test': instance.test.name,
            'questions_count': instance.test.questions_count,
            'active_questions_count': instance.test.questions.filter(active=True).count()
        }

        return {
            'id': instance.id,
            'test_data': test_data,
            'question': instance.question,
            'options_count': instance.options_count,
        }


class AnswerOptionSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = (
            'question',
            'option_text',
            'is_correct'
        )


    def validate(self, attrs):
        question = attrs['question']
        is_correct = attrs['is_correct']
        options_count = question.options.all().count()

        if question.options.count() == question.options_count - 1 \
                and not question.options.filter(is_correct=True).exists() and is_correct == False:
            raise serializers.ValidationError(
                {
                    'msg': "savolda bitta tog'ri javob bo'lishi shart"
                }
            )

        if question.options.filter(is_correct=True).exists() and is_correct == True:
            raise serializers.ValidationError(
                {
                    'msg': "Bitta savolda faqat bitta tog'ri variant bo'lishi mumkin"
                }
            )

        if options_count >= question.options_count:
            raise serializers.ValidationError(
                {
                    'msg': f"Bu savolda faqat {question.options_count} ta variantlar bo'lishi mumkin xolos"
                }
            )

        return attrs



    def to_representation(self, instance):
        question_data = {
            'id': instance.question.id,
            'question': instance.question.question,
            'options_count': instance.question.options_count,
            'active_options_count': instance.question.options.count()
        }
        return {
            'id': instance.id,
            'question_data':question_data,
            'option_text': instance.option_text,
            'is_correct': instance.is_correct,
        }

class AnswerOptionSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = (
            'option_text',
        )

class AnswerOptionSerializerForPutForAdmin(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = (
            'option_text',
            'is_correct'
        )

class UserTestSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = (
            'user',
            'test'
        )

    def validate(self, attrs):
        test = attrs['test']

        if not test.active:
            raise serializers.ValidationError(
                {
                    'msg': "Bu test hozirda aktiv emas"
                }
            )

        return attrs

class QuestionSerializerForUserTestResponse(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question',
        )

class UserResponsesSerializerForGet(serializers.ModelSerializer):
    question_data = QuestionSerializerForUserTestResponse(source='question')
    answer_option_data = AnswerOptionSerializerForGet(source='answer_option')
    class Meta:
        model = UserTestResponse
        fields = (
            'id',
            'question_data',
            'answer_option_data'
        )

class UserTestSerializerForGet(serializers.ModelSerializer):
    user_data = UserSerializer(source='user')
    test_data = TestSerializerForList(source='test')
    class Meta:
        model = UserTest
        fields = (
            'id',
            'user_data',
            'test_data',
            'status',
            'result',
            'completed_data',
        )

class UserTestSerializerForGetStudent(serializers.ModelSerializer):
    test_data = TestSerializerForList(source='test')
    responses = UserResponsesSerializerForGet(source='responses')
    class Meta:
        model = UserTest
        fields = (
            'id',
            'test_data',
            'status',
            'result',
            'completed_data',
            'responses'
        )


class UserTestResponseSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UserTestResponse
        fields = (
            'user_test',
            'question',
            'answer_option'
        )

    def validate(self, attrs):
        user = self.context['request'].user
        user_test = attrs['user_test']
        question = attrs['question']
        answer_option = attrs['answer_option']

        test = user_test.test

        if user_test.user != user:
            raise serializers.ValidationError(
                {
                    'msg': f"Siz bu testga javob bera olmeysiz"
                }
            )

        if question.test != test:
            raise serializers.ValidationError(
                {
                    'msg': f"{test.name} testida bunday savol mavjud emas"
                }
            )

        if answer_option.question != question:
            raise serializers.ValidationError(
                {
                    'msg': f"{question.question} savolida bunday variant mavjud emas"
                }
            )

        return attrs


class UserTestResponseSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = UserTestResponse
        fields = (
            'question',
            'answer_option'
        )

    def validate(self, attrs):
        user_test = self.instance.user_test
        question = attrs['question']
        answer_option = attrs['answer_option']

        test = user_test.test

        if user_test.status == "completed":
            raise serializers.ValidationError(
                {
                    'msg': f"Yakunlangan testingiz javoblarini ozgartira olmaysiz"
                }
            )

        if question.test != test:
            raise serializers.ValidationError(
                {
                    'msg': f"{test.name} testida bunday savol mavjud emas"
                }
            )

        if answer_option.question != question:
            raise serializers.ValidationError(
                {
                    'msg': f"{question.question} savolida bunday variant mavjud emas"
                }
            )

        return attrs

class UserTestResponseSerializerForGet(serializers.ModelSerializer):
    question_data = QuestionSerializerForGet(source='question')
    answer_option_data = AnswerOptionSerializerForGet(source='answer_option')
    class Meta:
        model = UserTestResponse
        fields = (
            'id',
            'question_data',
            'answer_option_data'
        )








