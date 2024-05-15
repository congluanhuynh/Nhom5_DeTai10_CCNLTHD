from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import Thesis, Major, Department, Student, User, Score, Council, CouncilMembership, InterviewSchedule


class BaseSerializer(ModelSerializer):
    image = SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/static/%s" % obj.image.name


class MajorSerializer(ModelSerializer):

    class Meta:
        model = Major
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class ThesisSerializer(ModelSerializer):
    class Meta:
        model = Thesis
        fields = ["id", "name", "created_date", "major"]


class InterviewScheduleSerializer(ModelSerializer):
    class Meta:
        model = InterviewSchedule
        fields = ["council","thesis","date", "time","location"]


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ["username", "first_name", "last_name", "school_year", "major"]


class CouncilSerializer(ModelSerializer):
    class Meta:
        model = Council
        fields = ["name", "department", "members"]


class CouncilMembershipSerializer(ModelSerializer):
    class Meta:
        model = CouncilMembership
        fields = ["user","council", "role"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'score']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'score_value']

