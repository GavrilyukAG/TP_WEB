import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askga.settings")
django.setup()


from service.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
from faker import Faker
import random


fake = Faker()


def create_users(n):
    for _ in range(n):
        u = User.objects.create_user(username=fake.user_name(),
                                     email=fake.email(),
                                     password="061297sg"
                                     )
        u.save()
        p = Profile.objects.create(user=u,
                                   rating=random.randint(0, 5),
                                   )
        p.save()


def create_tags(n):
    for _ in range(n):
        t = Tag(title=fake.word())
        t.save()


def create_questions(n):
    profile_id_list = list(Profile.objects.values_list('pk', flat=True))
    tags_list = list(Tag.objects.values_list('pk', flat=True))
    for _ in range(n):
        p_id = Profile.objects.get(pk=profile_id_list[random.randint(0, len(profile_id_list)-1)])
        q = Question(author=p_id,
                     title=fake.sentence(),
                     text=fake.text(),
                     rating=random.randint(-1, 20)
                     )
        q.save()
        for _ in range(random.randint(1, 5)):
            t_id = Tag.objects.get(id=tags_list[random.randint(0, len(tags_list)-1)])
            q.tags.add(t_id)

        q.save()

        create_answers(random.randint(1, 10), q)
        create_like(p_id, q)


def create_answers(n, question_id):
    profile_id_list = list(Profile.objects.values_list('pk', flat=True))
    for _ in range(n):
        p_id = Profile.objects.get(pk=profile_id_list[random.randint(0, len(profile_id_list)-1)])
        a = Answer(author=p_id,
                   question=question_id,
                   text=fake.text()
                   )
        a.save()


def create_like(profile_id, question_id):  #get_or_create
    try:
        like = Like.objects.get(user=profile_id, question=question_id)
    except:
        like = Like.objects.create(user=profile_id,
                    question=question_id,
                    is_vote=random.choice([0,1])
                    )
        like.save()



# create_users(2)
# create_tags(20)
# create_questions(1)