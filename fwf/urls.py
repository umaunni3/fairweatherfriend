from django.urls import path, include

from django.contrib import admin
from django.conf.urls import url

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("db2/", hello.views.db, name="db2"),
    path("whoami/", hello.views.whoami, name="whoami"),
    url(r'api/register_weather_rating/(?P<pk>[0-9]+)', hello.views.register_weather_rating),
    path("options/", hello.views.options, name="options"),
    url(r'options/choose_profile/(?P<pk>[a-z]+)', hello.views.set_user_profile),
    path("options/clear_records/", hello.views.delete_user_records, name="clear_records"),
]
