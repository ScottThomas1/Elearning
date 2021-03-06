"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from courses.views import (course_add, do_section, do_test, show_results, SectionViewSet,
                           course_detail, CourseListView) #CourseDetailView
from students.views import student_detail, student_page, public_page
from api.views import UserViewSet
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sections', SectionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^course_detail/(?P<course_id>\d+)/$', course_detail,
        name='course_detail'),
    # url(r'^course_detail/(?P<pk>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^course_add/$', course_add, name='course_add'),
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^section/(?P<section_id>\d+)/$', do_section, name='do_section'),
    url(r'^section/(?P<section_id>\d+)/test/$', do_test, name='do_test'),

    url(r'^section/(?P<section_id>\d+)/results/$', show_results, name='show_results'),
    url(r'^student_detail/$', student_detail, name='student_detail'),
    url(r'^api/', include(router.urls)),
    url(r'^$', CourseListView.as_view(), name='course_list'),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^student_page/$', student_page, name='student_page'),
    url(r'^public_page/$', public_page, name='public_page'),
]
# url('^', include('django.contrib.auth.urls', namespace='auth')), second url pattern
# url(r'^accounts/next/$', auth_views.LoginView.as_view()),

if settings.DEBUG:
  import debug_toolbar
  urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
  ] + urlpatterns
