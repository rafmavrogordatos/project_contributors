from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Skill, Project, Application, Collaborator
from .serializers import (
    UserSerializer,
    SkillSerializer,
    ProjectSerializer,
    ApplicationSerializer,
    CollaboratorSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        """Generate password reset token and store timestamp."""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "No user found with this email."}, status=status.HTTP_404_NOT_FOUND)

        # Generate reset token
        token = default_token_generator.make_token(user)
        user.reset_password_token = token
        user.reset_password_timestamp = timezone.now()
        user.save()

        return Response({
            "message": "Password reset token generated successfully.",
            "token": token  # Only for testing; in production, email this instead.
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='reset-password-confirm')
    def reset_password_confirm(self, request):
        """Confirm new password using token."""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        user = User.objects.filter(reset_password_token=token).first()

        if not user:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if token has expired (e.g., 1 hour expiration)
        time_difference = timezone.now() - user.reset_password_timestamp
        if time_difference.total_seconds() > 3600:
            return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.reset_password_token = None
        user.reset_password_timestamp = None
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        skill = self.get_object()
        if skill.user != request.user:
            raise PermissionDenied("You can only delete your own skills.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def options(self, request):
        """Return available programming languages and skill levels"""
        data = {
            "languages": [lang[0] for lang in Skill.LANGUAGES],
            "levels": dict(Skill.LEVELS)  
        }
        return Response(data)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.prefetch_related("collaborators")

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator != request.user:
            raise PermissionDenied("You can only edit projects you created.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator != request.user:
            raise PermissionDenied("You can only delete projects you created.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        """Allow users to apply for a project."""
        project = self.get_object()

        if request.user == project.creator:
            return Response({"error": "You cannot apply to your own project."}, status=status.HTTP_400_BAD_REQUEST)

        if project.collaborators.filter(user=request.user).exists():
            return Response({"error": "You are already a collaborator in this project."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Application.objects.filter(applicant=request.user, project=project).exists():
            return Response({"error": "You have already applied to this project."}, status=status.HTTP_400_BAD_REQUEST)
        
        if project.collaborators.count() >= project.max_collaborators:
            return Response({"error": "Project has reached max collaborators."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not project.is_open_for_collaboration:
            return Response({"error": "Project is not open for collaboration."}, status=status.HTTP_400_BAD_REQUEST)
        
        application = Application.objects.create(
            applicant=request.user, project=project, message=request.data.get("message", "")
        )
        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def applications(self, request, pk=None):
        """List all applications to a project."""
        project = self.get_object()
        applications = project.applications.all()
        return Response(ApplicationSerializer(applications, many=True).data)
    
    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def collaborators(self, request, pk=None):
        """List all collaborators of a project."""
        project = self.get_object()
        collaborators = project.collaborators.all()
        return Response(CollaboratorSerializer(collaborators, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def open_projects(self, request):
        """Retrieve projects with available slots."""
        open_projects = Project.objects.annotate(
            current_collaborators_count=Count("collaborators", distinct=True)
        ).filter(current_collaborators_count__lt=models.F("max_collaborators"))

        return Response(ProjectSerializer(open_projects, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def user_stats(self, request):
        """Retrieve user statistics."""
        
        user = request.user

        return Response(
            {
                "projects_created": Project.objects.filter(creator=user).count(),
                "projects_contributed": Collaborator.objects.filter(user=user).count(),
            }
        )

class ApplicationViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin):
    """ViewSet for listing and viewing applications, with accept/decline actions."""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Show only applications related to the user (applicant or project owner)."""
        user = self.request.user
        return Application.objects.filter(
            models.Q(applicant=user) | models.Q(project__creator=user)
        ).select_related("applicant", "project")

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        """Accept a project application."""
        try:
            application = Application.objects.get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

        project = application.project

        if request.user != project.creator:
            raise PermissionDenied("Only the project owner can accept applications.")

        if application.status != "pending":
            return Response({"error": "Application has already been processed."}, status=status.HTTP_400_BAD_REQUEST)

        if project.collaborators.filter(user=application.applicant).exists():
            return Response({"error": "User is already a collaborator."}, status=status.HTTP_400_BAD_REQUEST)

        if project.collaborators.count() >= project.max_collaborators:
            return Response({"error": "Project has reached max collaborators."}, status=status.HTTP_400_BAD_REQUEST)

        application.accept()
        Collaborator.objects.get_or_create(user=application.applicant, project=project)

        return Response({"message": "Application accepted. User added as collaborator."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def decline(self, request, pk=None):
        """Decline a project application."""
        try:
            application = Application.objects.get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

        project = application.project

        if request.user != project.creator:
            raise PermissionDenied("Only the project owner can decline applications.")

        if application.status != "pending":
            return Response({"error": "Application has already been processed."}, status=status.HTTP_400_BAD_REQUEST)

        application.decline()
        return Response({"message": "Application declined."}, status=status.HTTP_200_OK)