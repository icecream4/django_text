#Скрипт по заполнению базы.
from text.models import Text, UserProfile, Comment, Like
from django.contrib.contenttypes.models import ContentType
import datetime
import random
import json


def fill_users(num=0):
    f = open('person.json')
    person = json.load(f)
    person_len = len(person)
    f.close()

    f = open('names.json')
    names = json.load(f)
    names_len = len(names)
    f.close()

    insert_list = []

    rand_names_1 = random.sample(names, num)
    rand_names_2 = random.sample(names, num)
    for i in range(num):
        a = UserProfile()
        a.set_password('qwerty')
        a.username = rand_names_1[i] + '_' + rand_names_2[i]
        a.email = person[random.randint(1, person_len) - 1]['email']
        a.birth_date = person[random.randint(1, person_len) - 1]['birth_date']
        a.contents = person[random.randint(1, person_len) - 1]['contents']
        insert_list.append(a)
    UserProfile.objects.bulk_create(insert_list)



def fill_text(num=0):
    users = UserProfile.objects.values_list('id', flat=True)
    
    f = open('contents.json')
    content = json.load(f)
    content_len = len(content)

    insert_list = []

    for i in range(num):
        a = Text()
        a.title = content[random.randint(1, content_len) - 1]['title']
        a.author_id = random.choice(users)
        a.text_type = random.randint(1, (len(Text.TYPE_CHOICE))) - 1
        a.created_at = content[random.randint(1, content_len) - 1]['created_at']
        a.contents = content[random.randint(1, content_len) - 1]['contents']
        a.views = 0
        insert_list.append(a)
    Text.objects.bulk_create(insert_list)


def fill_comment(num=0):
    users = UserProfile.objects.values_list('id', flat=True)
    text = Text.objects.values_list('id', flat=True)
    
    f = open('comments.json')
    comment = json.load(f)
    comment_len = len(comment)

    insert_list = []

    for i in range(num):
        a = Comment()
        a.author_id = random.choice(users)
        a.post_id = random.choice(text)
        a.contents = comment[random.randint(1, comment_len) - 1]['comments']
        insert_list.append(a)
    Comment.objects.bulk_create(insert_list)

def fill_like(num1=0, num2=0):
    users = UserProfile.objects.values_list('id', flat=True)
    text = Text.objects.values_list('id', flat=True)
    comment = Comment.objects.values_list('id', flat=True)
    
    insert_list = []

    model_type = ContentType.objects.get_for_model(Text)
    for i in range(num1):
        a = Like()
        a.author_id = random.choice(users)
        a.object_id = random.choice(text)
        a.content_type = model_type
        insert_list.append(a)
    Like.objects.bulk_create(insert_list)

    insert_list = []

    model_type = ContentType.objects.get_for_model(Comment)
    for i in range(num2):
        a = Like()
        a.author_id = random.choice(users)
        a.object_id = random.choice(comment)
        a.content_type = model_type
        insert_list.append(a)
    Like.objects.bulk_create(insert_list)