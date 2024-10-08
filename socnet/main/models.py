from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db import models



class User(AbstractUser):
    ''' Добавление поля к базовой таблице User'''

    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions", blank=True
    )


class PrivacyLevel(models.Model):
    ''' Таблица приватности'''

    PUBLIC = "public"
    PRIVATE = "private"
    FRIENDS_ONLY = "friends_only"

    PRIVACY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
        (FRIENDS_ONLY, "Friends Only"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Interest(models.Model):
    ''' Таблица интересы'''

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def get_default_privacy_level():
    return PrivacyLevel.objects.get(id=1)


class Profile(models.Model):
    ''' Таблица профиля'''

    firstname = models.CharField(max_length=255)
    lastname = models.TextField()
    age = models.IntegerField(blank=True, null=True)  # Необязательное поле
    gender = models.CharField(
        max_length=50, blank=True, null=True
    )  # Необязательное поле
    location = models.CharField(
        max_length=255, blank=True, null=True
    )  # Необязательное поле
    link = models.TextField(blank=True, null=True)  # Необязательное поле
    settings = models.CharField(
        max_length=255, blank=True, null=True
    )  # Необязательное поле
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privacy = models.ForeignKey(
        PrivacyLevel,
        on_delete=models.SET_NULL,
        null=True,
        default=get_default_privacy_level,
    )
    interests = models.ManyToManyField(Interest, blank=True)  # Необязательное поле

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def is_friend_with(self, other_profile):
        return Friendship.objects.filter(
            (
                Q(profile_one=self, profile_two=other_profile)
                | Q(profile_one=other_profile, profile_two=self)
            ),
            status="friends",
        ).exists()


class Mediafile(models.Model):
    ''' Таблица медиафайлов'''

    profile = models.ForeignKey(
        Profile, related_name="media_files", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="media/")
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(
        max_length=50,
        choices=[
            ("avatar", "Avatar"),
            ("video", "Video"),
            ("other", "Other"),
            ("image", "Image"),
        ],
    )
    description = models.TextField()


class FriendshipStatus(models.Model):
    ''' Таблица статусов дружбы'''

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Friendship(models.Model):
    ''' Таблица дружбы'''

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(FriendshipStatus, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    profile_one = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="friendships_initiated",
    )
    profile_two = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="friendships_received",
    )


class Mail(models.Model):
    ''' Таблица почты'''

    sender = models.ForeignKey(
        Profile, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    is_read = models.BooleanField(default=False)
    is_deleted_sender = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content}"


class Group(models.Model):
    ''' Таблица группы'''

    PUBLIC = "public"
    PRIVATE = "private"
    SECRET = "secret"

    GROUP_TYPES = [(PUBLIC, "Public"), (SECRET, "Secret"), (PRIVATE, "Private")]
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to="group_photos/", blank=True, null=True)
    group_type = models.CharField(max_length=10, choices=GROUP_TYPES, default=PUBLIC)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rules = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Status(models.Model):
    ''' Таблица статус'''

    ADMIN = "admin"
    USER = "user"

    STATUS_CHOICES = [
        (ADMIN, "Administrator"),
        (USER, "User"),
    ]
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, default=USER)

    def __str__(self):
        return f"{self.name} "


class GroupMembership(models.Model):
    ''' Таблица нахождения в группе'''

    profile = models.ForeignKey(
        Profile, related_name="group_memberships", on_delete=models.CASCADE
    )
    group = models.ForeignKey(Group, related_name="members", on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "group")

    def __str__(self):
        return f"{self.profile} {self.group} {self.status} {self.joined_at}"


class Tag(models.Model):
    ''' Таблица тэгов для новостей'''

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    ''' Таблица новостей'''

    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    profile = models.ForeignKey(
        Profile, related_name="news_posts", on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag, related_name="news_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ''' Таблица комментариев'''

    text = models.TextField()
    author = models.ForeignKey(
        Profile, related_name="comments", on_delete=models.CASCADE
    )
    news = models.ForeignKey(News, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.news} - {self.text[:20]}"

    class Meta:
        ordering = ["created_at"]  # Сортировка комментариев по дате создания

    def is_parent(self):
        """Проверяет, является ли комментарий родительским."""
        return self.parent is None

    def get_replies(self):
        """Возвращает все ответы на комментарий."""
        return Comment.objects.filter(parent=self)


class Reaction(models.Model):
    ''' Таблица реакций на новости'''

    LIKE = "like"
    DISLIKE = "dislike"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ("profile", "content_type", "object_id", "reaction_type")


class StatusProfile(models.Model):
    ''' Таблица статусов пользователя'''

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    is_busy = models.BooleanField(default=False)
    do_not_disturb = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    ''' Таблица для чата'''

    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.TextField()
    profile = models.ForeignKey(
        Profile, related_name="chat_message", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, related_name="chat_members", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Сообщение от {self.profile} от {self.created_at} "


class Notification(models.Model):
    ''' Таблица для нотификаций для АПИ'''

    FRIEND_REQUEST = "FR"
    MESSAGE = "MSG"
    MENTION = "MENT"

    NOTIFICATION_CHOICES = [
        (FRIEND_REQUEST, "Friend Request"),
        (MESSAGE, "Message"),
        (MENTION, "Mention"),
    ]

    profile = models.ForeignKey(
        Profile, related_name="notifications", on_delete=models.CASCADE
    )
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class ActivityLog(models.Model):
    ''' Таблица активности для АПИ'''

    LOGIN = "LOGIN"
    POST = "POST"
    COMMENT = "COMMENT"
    LIKE = "LIKE"

    ACTION_CHOICES = [
        (LOGIN, "Login"),
        (POST, "Post Created"),
        (COMMENT, "Comment Made"),
        (LIKE, "Like"),
    ]

    profile = models.ForeignKey(
        Profile, related_name="activities", on_delete=models.CASCADE
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification_norest(models.Model):
    ''' Таблица нотификаций (активности пользователя при регистрации/аутентификации)'''

    AUTHENTICATION = "AUTHENTICATION"
    OTHER = "OTHER"

    NOTIFICATION_CHOICES = [
        (AUTHENTICATION, "AUTHENTICATION"),
        (OTHER, "OTHER"),
    ]

    profile = models.ForeignKey(
        Profile, related_name="system_notifications", on_delete=models.CASCADE
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class ActivityLog_norest(models.Model):
    ''' Таблица активности (все реакции/создании группы и т.д)'''

    NEWS = "NEWS"
    GROUP = "GROUP"
    PROFILE = "PROFILE"
    MAIL = "MAIL"
    FRIEND = "FRIEND"

    ACTION_CHOICES = [
        (NEWS, "NEWS"),
        (GROUP, "GROUP"),
        (PROFILE, "PROFILE"),
        (MAIL, "MAIL"),
        (FRIEND, "FRIEND"),
    ]

    profile = models.ForeignKey(
        Profile, related_name="user_activities", on_delete=models.CASCADE
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ArchivedMail(models.Model):
    ''' Таблица для хранения не актуальных данных из почты'''

    sender = models.ForeignKey(
        Profile, related_name="archived_sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="archived_received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="archived_replies",
    )
    is_read = models.BooleanField(default=False)
    is_deleted_sender = models.BooleanField(default=False)
    archived_at = models.DateTimeField(auto_now_add=True)


class ArchiveChat(models.Model):
    ''' Таблица для хранения не актуальных данных из чата'''

    profile = models.ForeignKey(
        Profile, related_name="archived_chat_messages", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, related_name="archived_chat_members", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField()
    archived_at = models.DateTimeField(auto_now_add=True)
