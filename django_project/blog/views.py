from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from users.models import Profile
from .backend.backend import *
from .forms import *


@login_required
def pin_post(request, classroom_id, forum_id, post_id):
    print("request", request)
    print(Post.objects.all().count())
    for p in Post.objects.all():
        p.unpin()
    post = Post.objects.filter(id=post_id).first()
    post.pin()
    return redirect('/dashboard/classroom/' + str(classroom_id) + '/' + str(forum_id))


@login_required
def unpin_post(request, classroom_id, forum_id, post_id):
    print("request", request)
    post = get_object_or_404(Post, id=post_id)
    post.unpin()
    return redirect('/dashboard/classroom/' + str(classroom_id) + '/' + str(forum_id))


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required()
def dashboard(request):
    return render(request, 'blog/dashboard.html', {'classrooms': get_classrooms(request.user),
                                                   'type': Profile.objects.get(user_id=request.user).type})


@login_required()
def classroom(request, classroom_id):
    if match(user=request.user, classroom_id=classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)
        return render(request, 'blog/classroom.html',
                      {'exams': get_exams(classroom), 'forums': get_forums(classroom), 'classroom': classroom})
    else:
        messages.error(request, 'Sorry, We found out that you are not a member of the classroom!')
        return redirect('dashboard')


@login_required()
def create_classroom(request):
    if request.method == 'POST':
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            form = form.save()
            form.teacher = Profile.objects.get(user_id=request.user).user
            form.save()
            messages.success(request, f'Class has been created!')
            return redirect('dashboard')  # TODO except dashboard it should redirect to class's page
    else:
        form = ClassCreationForm()
    if Profile.objects.get(user_id=request.user).type == 'teacher':
        return render(request, 'blog/create_classroom.html', {'form': form})
    else:
        return render(request, 'blog/404.html', {})


@login_required()
def join_classroom(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if request.user in Classroom.objects.get(id=id).students.all():
            messages.error(request, 'you are already in this class!')
            return redirect('dashboard')  # TODO except dashboard it should redirect to class's page
        else:
            Classroom.objects.get(id=id).students.add(request.user)
            messages.success(request, 'you have been successfully added!')
            return redirect('dashboard')  # TODO except dashboard it should redirect to class's page
    else:
        if Profile.objects.get(user_id=request.user).type == 'student':
            return render(request, 'blog/join_classroom.html', {'classrooms': Classroom.objects.all()})
        else:
            return render(request, 'blog/404.html', {})


@login_required()
def forum(request, classroom_id, forum_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if request.FILES:
            file_filed = request.FILES['file']
        else:
            file_filed = None
        create_post(content, request.user, forum_id, file_filed)

    if match(user=request.user, classroom_id=classroom_id, forum_id=forum_id):
        forum = get_forums(Classroom.objects.get(id=classroom_id)).get(id=forum_id)
        return render(request, 'blog/forum.html', {'posts': get_posts(forum), 'url': settings.MEDIA_ROOT})
    else:
        messages.error(request, 'Something went wrong!')
        return redirect('dashboard')


@login_required()
def create_forum(request, classroom_id):
    if request.method == 'POST':
        form = ForumCreationForm(request.POST)
        if form.is_valid():
            form = form.save()
            form.classroom = Classroom.objects.get(id=classroom_id)
            form.save()
            messages.success(request, f'Forum has been created!')
            return redirect('/dashboard/classroom/' + str(classroom_id))
    else:
        form = ForumCreationForm()
    return render(request, 'blog/create_forum.html', {'form': form})


@login_required()
def create_exam(request, classroom_id):
    if request.method == 'POST':
        form = ExamCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            form.classroom = Classroom.objects.get(id=classroom_id)
            form.save()
            messages.success(request, f'exam has been created!')
            return redirect('/dashboard/classroom/' + str(classroom_id))
    else:
        form = ExamCreationForm()
    if Profile.objects.get(user_id=request.user).type == 'teacher':
        return render(request, 'blog/create_exam.html', {'form': form})
    else:
        return render(request, 'blog/404.html', {})


@login_required()
def exam_page(request, classroom_id, exam_id):
    if request.method == 'GET':
        if match(user=request.user, classroom_id=classroom_id, exam_id=exam_id):
            if Profile.objects.get(user_id=request.user).type == 'student':
                exam = get_exams(Classroom.objects.get(id=classroom_id)).get(id=exam_id)
                form = ResponseForm()
                return render(request, 'blog/exam.html', {'exam': exam, 'url': settings.MEDIA_ROOT, 'form': form})
            elif Profile.objects.get(user_id=request.user).type == 'teacher':
                exam = get_exams(Classroom.objects.get(id=classroom_id)).get(id=exam_id)
                return render(request, 'blog/teacher_exam.html',
                              {'exam': exam, 'url': settings.MEDIA_ROOT, 'responses': get_responses(exam)})
        else:
            messages.error(request, 'Something went wrong!')
            return redirect('dashboard')
    elif request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid() or match(user=request.user, classroom_id=classroom_id, exam_id=exam_id):
            form = form.save(commit=False)
            form.student = request.user
            form.exam = get_exams(Classroom.objects.get(id=classroom_id)).get(id=exam_id)
            form.save()
            messages.success(request, f'your response sent successfully!')
            return redirect('/dashboard/classroom/' + str(classroom_id))
        else:
            messages.error(request, 'Something went wrong!')
            return redirect('dashboard')
