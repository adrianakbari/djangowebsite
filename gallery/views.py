from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import GalleryForm
from .models import Gallery, GalleryView
from marketing.forms import EmailSignupForm
from marketing.models import Signup

form = EmailSignupForm()
anonymousUser = get_user_model()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


# class SearchView(View):
#     def get(self, request, *args, **kwargs):
#         queryset = Gallery.objects.all()
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

# # Search view needs to be centralized in the end
# def search(request):
#     queryset = Gallery.objects.all()
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


# def get_category_count():
#     queryset = Gallery \
#         .objects \
#         .values('categories__title') \
#         .annotate(Count('categories__title'))
#     return queryset


class GalleryListView(ListView):
    form = EmailSignupForm()
    model = Gallery
    template_name = 'gallery.html'
    context_object_name = 'queryset'
    queryset = Gallery.objects.order_by('-timestamp')[:3]
    paginate_by = 1

    def get_context_data(self, **kwargs):
        # category_count = get_category_count()
        most_recent = Gallery.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        # context['category_count'] = category_count
        context['form'] = self.form
        return context


# def post_list(request):
#     category_count = get_category_count()
#     most_recent = Gallery.objects.order_by('-timestamp')[:3]
#     post_list = Gallery.objects.all()
#     paginator = Paginator(post_list, 4)
#     page_request_var = 'page'
#     page = request.GET.get(page_request_var)
#     try:
#         paginated_queryset = paginator.page(page)
#     except PageNotAnInteger:
#         paginated_queryset = paginator.page(1)
#     except EmptyPage:
#         paginated_queryset = paginator.page(paginator.num_pages)

#     context = {
#         'queryset': paginated_queryset,
#         'most_recent': most_recent,
#         'page_request_var': page_request_var,
#         'category_count': category_count,
#         'form': form
#     }
#     return render(request, 'blog.html', context)


class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'gallery_post.html'
    context_object_name = 'post'
    # form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            GalleryView.objects.get_or_create(
                user=self.request.user,
                gallery_post=obj
            )
            viewCount = GalleryView.objects.filter(
                user_id=self.request.user.id, gallery_post_id=obj.id)[0].view_count
            GalleryView.objects.filter(
                user_id=self.request.user.id, gallery_post_id=obj.id).update(view_count=viewCount+1)
        else:
            GalleryView.objects.get_or_create(
                user=anonymousUser.objects.get(pk=2),
                gallery_post=obj
            )
            viewCount = GalleryView.objects.filter(
                user_id=2, gallery_post_id=obj.id)[0].view_count
            GalleryView.objects.filter(
                user_id=2, gallery_post_id=obj.id).update(view_count=viewCount+1)
        return obj

    def get_context_data(self, **kwargs):
        # category_count = get_category_count()
        obj = super().get_object()
        most_recent = Gallery.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['view_count'] = obj.view_count
        # context['form'] = self.form
        return context

    # def post(self, request, *args, **kwargs):
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         post = self.get_object()
    #         form.instance.user = request.user
    #         form.instance.post = post
    #         form.save()
    #         return redirect(reverse("post-detail", kwargs={
    #             'pk': post.pk
    #         }))


# def post_detail(request, id):
#     category_count = get_category_count()
#     most_recent = Gallery.objects.order_by('-timestamp')[:3]
#     post = get_object_or_404(Gallery, id=id)

#     if request.user.is_authenticated:
#         GalleryView.objects.get_or_create(user=request.user, post=post)

#     form = CommentForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             form.instance.user = request.user
#             form.instance.post = post
#             form.save()
#             return redirect(reverse("post-detail", kwargs={
#                 'id': post.pk
#             }))
#     context = {
#         'post': post,
#         'most_recent': most_recent,
#         'category_count': category_count,
#         'form': form
#     }
#     return render(request, 'post.html', context)


# class GalleryCreateView(CreateView):
#     model = Gallery
#     template_name = 'gallery_post_create.html'
#     form_class = GalleryForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Create'
#         return context

#     def form_valid(self, form):
#         form.instance.author = get_author(self.request.user)
#         form.save()
#         return redirect(reverse("gallery-post-detail", kwargs={
#             'pk': form.instance.pk
#         }))


# def post_create(request):
#     title = 'Create'
#     form = GalleryForm(request.POST or None, request.FILES or None)
#     author = get_author(request.user)
#     if request.method == "POST":
#         if form.is_valid():
#             form.instance.author = author
#             form.save()
#             return redirect(reverse("post-detail", kwargs={
#                 'id': form.instance.id
#             }))
#     context = {
#         'title': title,
#         'form': form
#     }
#     return render(request, "post_create.html", context)


class GalleryUpdateView(UpdateView):
    model = Gallery
    template_name = 'post_create.html'
    form_class = GalleryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        context['gallery_post_form'] = GalleryForm(instance=self.object)
        return context

    def form_valid(self, form):
        # form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("gallery-post-detail", kwargs={
            'pk': form.instance.pk
        }))


# def post_update(request, id):
#     title = 'Update'
#     post = get_object_or_404(Gallery, id=id)
#     form = GalleryForm(
#         request.POST or None,
#         request.FILES or None,
#         instance=post)
#     author = get_author(request.user)
#     if request.method == "POST":
#         if form.is_valid():
#             form.instance.author = author
#             form.save()
#             return redirect(reverse("post-detail", kwargs={
#                 'id': form.instance.id
#             }))
#     context = {
#         'title': title,
#         'form': form
#     }
#     return render(request, "post_create.html", context)


class GalleryDeleteView(DeleteView):
    model = Gallery
    success_url = '/gallery'
    template_name = 'post_confirm_delete.html'


# def post_delete(request, id):
#     post = get_object_or_404(Gallery, id=id)
#     post.delete()
#     return redirect(reverse("post-list"))
