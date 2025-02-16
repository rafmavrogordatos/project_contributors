from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Skill, Project, Application, Collaborator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'age', 'country', 'residence']

    def create(self, validated_data):
        """Ensure password is hashed before saving"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Ensure password is hashed on update"""
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)
    
class SkillSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Skill
        fields = ['id', 'language', 'level', 'user']

    def validate(self, data):
        user = self.context["request"].user
        if user.skills.count() >= 3:
            raise serializers.ValidationError({
            'error': "You can only add up to 3 skills."
            })
        return data

class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    active_collaborators_count = serializers.IntegerField(source='active_collaborators', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'description', 'max_collaborators', 'creator', 'active_collaborators_count']

    def validate_max_collaborators(self, value):
        """Ensure max collaborators is at least 1."""
        if value < 1:
            raise serializers.ValidationError("max_collaborators must be at least 1.")
        return value

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.ReadOnlyField(source="applicant.username")
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'project', 'message', 'status', 'created_at']

    def validate(self, data):
        """Ensure user is not already a collaborator or has applied to the project."""
        project = data["project"]
        user = self.context["request"].user

        if project.collaborators.filter(user=user).exists():
            raise serializers.ValidationError("You are already a collaborator in this project.")

        if Application.objects.filter(applicant=user, project=project).exists():
            raise serializers.ValidationError("You have already applied to this project.")

        return data

class CollaboratorSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Collaborator
        fields = ['id', 'user', 'project', 'joined_at']
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value