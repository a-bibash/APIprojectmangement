from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Project, ProjectMember, Task, Comment

User = get_user_model()  # Get the custom user model


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


# ProjectMember Serializer
class ProjectMemberSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']



class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)  # Nested serializer for the owner field
    members = ProjectMemberSerializer(many=True, read_only=True)  # Assuming this is the correct relationship

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at']



class TaskSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=PRIORITY_CHOICES)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,  # Make it optional so it can default to the current user
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assigned_to', 'project', 'created_at', 'due_date',
        ]

    def create(self, validated_data):
        # Default `assigned_to` to the current user if not provided
        if 'assigned_to' not in validated_data:
            validated_data['assigned_to'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure updates to `assigned_to` follow the same logic as creation
        if 'assigned_to' not in validated_data:
            validated_data['assigned_to'] = self.context['request'].user
        return super().update(instance, validated_data)



# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Automatically populate the user
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())  # Reference task by ID

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']

    def create(self, validated_data):
        # Automatically associate the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        data['user'] = user
        return data
