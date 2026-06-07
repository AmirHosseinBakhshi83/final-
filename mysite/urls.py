"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include,reverse
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from exam.views import custom_404_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['website:home', 'accounts:login', 'accounts:signup']

    def location(self, item):
        return reverse(item)

sitemaps = {'static': StaticViewSitemap}


handler404 = custom_404_view

urlpatterns = [
    path ("", include('website.urls')),
    path("admin/", admin.site.urls),
    path("dashboard/", include('dashboard.urls')),
    path("exam/", include('exam.urls')),
    path ("account/", include('accounts.urls')),
    path ("report/", include('report.urls')),
    path ("profile/", include('personal.urls')),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]+ debug_toolbar_urls()


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]