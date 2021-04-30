from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import (
    search,
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete,
    IndexView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from marketing.views import email_list_signup, about, resume
from gallery.views import (
    GalleryListView,
    GalleryDetailView,
    GalleryUpdateView,
    GalleryDeleteView
)
from projects.views import (
    ProjectsListView,
    ProjectsDetailView,
    ProjectsUpdateView,
    ProjectsDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),
    path('', IndexView.as_view(), name='home'),
    path('search/', search, name='search'),
    path('about/', about, name='about'),
    path('resume/', resume, name='resume'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    # -----------Post Blog Urls-------------------
    # path('blog/', post_list, name='post-list'),
    path('blog/', PostListView.as_view(), name='blog-post-list'),
    # path('create/', PostCreateView.as_view(), name='post-create'),
    path('create/', post_create, name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('blog-post/<pk>/', PostDetailView.as_view(), name='blog-post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('blog-post/<pk>/update/',
         PostUpdateView.as_view(), name='blog-post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='blog-post-delete'),
    # -----------Gallery Urls-------------------
    path('gallery/', GalleryListView.as_view(), name='gallery-post-list'),
    path('gallery-post/<pk>/', GalleryDetailView.as_view(),
         name='gallery-post-detail'),
    path('gallery-post/<pk>/update/',
         GalleryUpdateView.as_view(), name='gallery-post-update'),
    path('gallery-post/<pk>/delete/',
         GalleryDeleteView.as_view(), name='gallery-post-delete'),
    # -----------Projects Urls-------------------
    path('projects/', ProjectsListView.as_view(), name='projects-post-list'),
    path('projects-post/<pk>/', ProjectsDetailView.as_view(),
         name='projects-post-detail'),
    path('projects-post/<pk>/update/',
         ProjectsUpdateView.as_view(), name='projects-post-update'),
    path('projects-post/<pk>/delete/',
         ProjectsDeleteView.as_view(), name='projects-post-delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
