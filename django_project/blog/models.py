from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Grade(models.TextChoices):
    ONE = "one"
    TWO = "two"
    THREE = 'three'
    FOUR = 'four'
    FIVE = 'five'
    SIX = 'six'
    SEVEN = 'seven'
    EIGHT = 'eight'
    NINE = 'nine'
    TEN_MATH = 'ten math'
    TEN_SCIENCE = 'ten science'
    TEN_HUMANITIES = 'ten humanities'
    ELEVEN_MATH = 'eleven math'
    ELEVEN_SCIENCE = 'eleven science'
    ELEVEN_HUMANITIES = 'eleven humanities'
    TWELVE_MATH = 'twelve math'
    TWELVE_SCIENCE = 'twelve science'
    TWELVE_HUMANITIES = 'twelve humanities'


class Classroom(models.Model):
    lesson = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, choices=Grade.choices)
    class_num = models.IntegerField()
    description = models.TextField(default="Welcome to this class!")
    students = models.ManyToManyField(User, related_name="classrooms_as_student", null=True)
    teacher = models.ForeignKey(User, related_name="classrooms_as_teacher", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.lesson


class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, related_name="forum_set")

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    file_field = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, verbose_name='post_file')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="post_set")
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def pin(self):
        self.pinned = True
        self.save()

    def unpin(self):
        self.pinned = False
        self.save()


class Exam(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    exam_file = models.FileField(upload_to='documents/%Y/%m/%d/')
    # mark of the students in this exam
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, related_name="exam_set")

    def __str__(self):
        return self.title


class Response(models.Model):
    id = models.BigAutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    response_file = models.FileField(upload_to='responses/%Y/%m/%d/', verbose_name="response")
    submit_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
