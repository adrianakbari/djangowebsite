from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Post, Author, PostView
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from gallery.models import Gallery
from projects.models import Project
from gallery.forms import GalleryForm
from projects.forms import ProjectsForm

form = EmailSignupForm()
anonymousUser = get_user_model()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


# class SearchView(View):
#     def get(self, request, *args, **kwargs):
#         queryset = Post.objects.all()
#         query = request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) |
#                 Q(overview__icontains=query)
#             ).distinct()
#         context = {
#             'queryset': queryset
#         }
#         return render(request, 'search_results.html', context)

# General Search
def search(request):
    # queryset = Post.objects.none()
    blogQueryset = Post.objects.none()
    galleryQueryset = Gallery.objects.none()
    projectsQueryset = Project.objects.none()

    if 'gen_qs' in request.GET:
        query = request.GET.get('gen_qs')
        blogQueryset = Post.objects.filter(Q(title__icontains=query) |
                                           Q(overview__icontains=query)).distinct()
        galleryQueryset = Gallery.objects.filter(Q(title__icontains=query) |
                                                 Q(overview__icontains=query)).distinct()
        projectsQueryset = Project.objects.filter(Q(title__icontains=query) |
                                                  Q(overview__icontains=query)).distinct()
    elif 'blog_qs' in request.GET:
        # search blog
        query = request.GET.get('blog_qs')
        blogQueryset = Post.objects.filter(Q(title__icontains=query) |
                                           Q(overview__icontains=query)).distinct()
    elif 'gallery_qs' in request.GET:
        # search gallery
        query = request.GET.get('gallery_qs')
        galleryQueryset = Gallery.objects.filter(Q(title__icontains=query) |
                                                 Q(overview__icontains=query)).distinct()
    elif 'projects_qs' in request.GET:
        # search projects
        query = request.GET.get('projects_qs')
        projectsQueryset = Project.objects.filter(Q(title__icontains=query) |
                                                  Q(overview__icontains=query)).distinct()
        # if query:
        #     queryset = queryset.filter(
        #         Q(title__icontains=query) |
        #         Q(overview__icontains=query)
        #     ).distinct()
    context = {
        # 'queryset': queryset
        'blogQueryset': blogQueryset,
        'galleryQueryset': galleryQueryset,
        'projectsQueryset': projectsQueryset
    }
    return render(request, 'search_results.html', context)

# Blog Search
# def blogSearch(request):
#     queryset = Post.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query) |
#             Q(overview__icontains=query)
#         ).distinct()
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        # featured = Post.objects.filter(featured=True)
        # latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            # 'object_list': featured,
            # 'latest': latest,
            'form': self.form
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")


# def index(request):
#     featured = Post.objects.filter(featured=True)
#     latest = Post.objects.order_by('-timestamp')[0:3]

#     if request.method == "POST":
#         email = request.POST["email"]
#         new_signup = Signup()
#         new_signup.email = email
#         new_signup.save()

#     context = {
#         'object_list': featured,
#         'latest': latest,
#         'form': form
#     }
#     return render(request, 'index.html', context)


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    queryset = Post.objects.order_by('-timestamp')[:3]
    paginate_by = 5

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context


def post_list(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
            viewCount = PostView.objects.filter(
                user_id=self.request.user.id, post_id=obj.id)[0].view_count
            PostView.objects.filter(
                user_id=self.request.user.id, post_id=obj.id).update(view_count=viewCount+1)
        else:
            PostView.objects.get_or_create(
                user=anonymousUser.objects.get(pk=2),
                post=obj
            )
            viewCount = PostView.objects.filter(
                user_id=2, post_id=obj.id)[0].view_count
            PostView.objects.filter(
                user_id=2, post_id=obj.id).update(view_count=viewCount+1)
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        context['view_count'] = Post.view_count
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog-post-detail", kwargs={
                'pk': post.pk
            }))


def post_detail(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog-post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog_post.html', context)


# class PostCreateView(CreateView):
#     model = Post
#     template_name = 'post_create.html'
#     form_class = PostForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Create'
#         context['blog_form'] = PostForm
#         # context['gallery_form'] = GalleryForm
#         # context['experience_form'] =
#         return context

#     def form_valid(self, form):
#         form.instance.author = get_author(self.request.user)
#         form.save()
#         return redirect(reverse("blog-post-detail", kwargs={
#             'pk': form.instance.pk
#         }))


def post_create(request):
    title = 'Create'
    post_form = PostForm(request.POST or None, request.FILES or None)
    gallery_post_form = GalleryForm(
        request.POST or None, request.FILES or None)
    projects_post_form = ProjectsForm(
        request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if post_form.is_valid():
            post_form.instance.author = author
            post_form.save()
            return redirect(reverse("blog-post-detail", kwargs={
                'pk': post_form.instance.pk
            }))
        elif gallery_post_form.is_valid():
            gallery_post_form.instance.author = author
            gallery_post_form.save()
            return redirect(reverse("gallery-post-detail", kwargs={
                'pk': gallery_post_form.instance.pk
            }))
        elif projects_post_form.is_valid():
            projects_post_form.instance.author = author
            projects_post_form.save()
            return redirect(reverse("projects-post-detail", kwargs={
                'pk': projects_post_form.instance.id
            }))
    context = {
        'title': title,
        'post_form': post_form,
        'gallery_post_form': gallery_post_form,
        'projects_post_form': projects_post_form
    }
    return render(request, "post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        context['post_form'] = PostForm(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("blog-post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog-post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("blog-post-list"))
