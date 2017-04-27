from django.conf.urls import url, patterns
import text.views as views
 # import text_list, text_detail, text_author, logout_author, login_author, registr_author, write_text, delete_text, delete_comment, put_like
# from django.contrib.auth.views import login

urlpatterns =  patterns(
	'text.views',
    url(r'^list/$', views.text_list, name='text_list'),
    url(r'^detail/(?P<text_id>\d+)/$', views.text_detail, name='text_detail'),

    url(r'^author/(?P<author_id>\d+)/$', views.text_author, name='text_author'),
    url(r'^author/write/$', views.write_text, name='write_text'),
    
    url(r'^registr/$', views.registr_author, name='registr_author'),
    url(r'^login/$', views.login_author, name='login_author'),
    
    url(r'^$', views.logout_author, name='logout_author'),
    url(r'^comment/(?P<text_id>\d+)/$', views.write_comment, name='write_comment'),
    url(r'^(?P<object_id>\d+)/(?P<text_id>\d+)/(?P<flag>\d+)/$', views.put_like, name='put_like'),
    
    url(r'^delete/(?P<text_id>\d+)/$', views.delete_text, name='delete_text'),
    url(r'^delete/(?P<text_id>\d+)/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    url(r'^delete/(?P<object_id>\d+)/(?P<text_id>\d+)/(?P<flag>\d+)/$', views.delete_like, name='delete_like'),
)
