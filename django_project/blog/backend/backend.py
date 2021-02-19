from ..models import Classroom, Forum, Post, Exam, Reply
from users.models import Profile


def create_new_classroom(lesson, grade, class_num, teacher, description=None):
    if description:
        classroom = Classroom(lesson=lesson, grade=grade, class_num=class_num, teacher=teacher)
    else:
        classroom = Classroom(lesson=lesson, grade=grade, class_num=class_num, teacher=teacher, description=description)
    classroom.save()


def add_student_to_classroom(classroom, student):
    student.classrooms_as_student.add(classroom)


def create_forum(title, classroom, description=None):
    if description:
        forum = Forum(title=title, classroom=classroom)
    else:
        forum = Forum(title=title, classroom=classroom, description=description)
    forum.save()


def create_post(content, author, forum_id, file_field):
    if match(user=author, forum_id=forum_id):
        post = Post(content=content, file_field=file_field, author=author, forum=Forum.objects.get(id=forum_id))
        post.save()
        print("post created")
    else:
        print("some problem authenticating")


def create_reply(content, author, forum_id, post_id):
    if match(user=author, forum_id=forum_id, post_id=post_id):
        reply = Reply(content=content, author=author, post=Post.objects.get(id=post_id))
        reply.save()
        print("post created")
    else:
        print("some problem authenticating")


def create_exam(title, exam_file, classroom, description=None):
    if description:
        exam = Exam(title=title, exam_file=exam_file, classroom=classroom, description=description)
    else:
        exam = Exam(title=title, exam_file=exam_file, classroom=classroom)
    exam.save()


def get_classrooms(user):
    if Profile.objects.get(user_id=user).type == "teacher":
        return user.classrooms_as_teacher.all()
    else:
        # student
        return user.classrooms_as_student.all()


def get_forums(classroom):
    return classroom.forum_set.all()


def get_exams(classroom):
    return classroom.exam_set.all()


def get_responses(exam):
    return sorted(exam.response_set.all(), key=lambda x: x.submit_time)


def get_response_belongs_student(exam, user):
    responses = sorted(exam.response_set.all(), key=lambda x: x.submit_time)
    for response in responses:
        if response.student == user:
            return response


def get_posts(forum):
    posts = []
    for post in sorted(forum.post_set.all(), key=lambda x: x.date_posted):
        posts.append(PostDTO(post, sorted(post.reply_set.all(), key=lambda x: x.date_posted)))

    return posts


def exam_belongs_to_classroom(classroom_id, exam_id):
    return Exam.objects.get(id=exam_id).classroom.id == classroom_id


def forum_belongs_to_classroom(classroom_id, forum_id):
    return Forum.objects.get(id=forum_id).classroom.id == classroom_id


def is_member_of_classroom(user, classroom_id):
    return classroom_id in [classroom.id for classroom in get_classrooms(user)]


def match(user=None, classroom_id=None, forum_id=None, exam_id=None, post_id=None):
    ans = True
    # return false if given ids are erroneous
    try:
        if classroom_id:
            Classroom.objects.get(id=classroom_id)
        if forum_id:
            Forum.objects.get(id=forum_id)
        if exam_id:
            Exam.objects.get(id=exam_id)
        if post_id:
            Post.objects.get(id=post_id)
    except:
        return False

    if classroom_id and user:
        ans = ans and is_member_of_classroom(user, classroom_id)
    if classroom_id and forum_id:
        ans = ans and forum_belongs_to_classroom(classroom_id, forum_id)
    if classroom_id and exam_id:
        ans = ans and exam_belongs_to_classroom(classroom_id, exam_id)
    return ans


class PostDTO:
    def __init__(self, post, replies=None):
        self.id = post.id
        self.content = post.content
        self.file_field = post.file_field
        self.date_posted = post.date_posted
        self.author = post.author
        self.forum = post.forum
        self.pinned = post.pinned
        self.replies = replies
