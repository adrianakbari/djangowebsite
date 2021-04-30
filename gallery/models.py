from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Author

User = get_user_model()


class GalleryView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gallery_post = models.ForeignKey('Gallery', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# class GalleryAuthor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField()

#     def __str__(self):
#         return self.user.username


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery-post-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('gallery-post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('gallery-post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def view_count(self):
        count = 0
        posts = GalleryView.objects.filter(gallery_post=self)
        for p in posts:
            count = count+p.view_count
        return count
