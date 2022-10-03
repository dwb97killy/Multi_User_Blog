from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from Blog.models import BlogContext, Comments
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from Blog.forms import BlogContextForm, CommentsForm, UserForm, UserProfileInfoForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.contrib.auth.models import User
# Create your views here.
'''
关于blog的操作
'''
'''
不需要用户登录就能操作
'''
class About(generic.TemplateView):
    template_name = 'blog/about.html'


class Post(generic.ListView):
    #ListView中的templates中需要导入的参数名预设值为model名字的小写加上_list，所以在这里是blogcontext_list
    model = BlogContext
    template_name = 'blog/index.html'
    def get_queryset(self):
        return BlogContext.objects.filter(publish_time__lte=timezone.now()).order_by('-publish_time')  # __lte是指less or equal to；-意味着按照递减序列排序


class Details(generic.DetailView):
    #DetailView中的templates中需要导入的参数名预设值为model名字的小写，所以在这里是blogcontext
    model = BlogContext
    template_name = 'blog/details.html'


'''
需要用户登录才能操作
'''
class CreateBlog(LoginRequiredMixin, generic.CreateView):  # Django通过继承LoginRequiredMixin类来限制用户登录，必须是第一个继承，在继承列表最左侧位置
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    form_class = BlogContextForm
    model = BlogContext
    template_name = "blog/create_blog.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点
    # success_url = reverse_lazy("home_page")
    def form_valid(self, form):  # 设置外键的值，将目前用户和发的blog关联起来
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class UpdateBlog(LoginRequiredMixin, generic.UpdateView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    form_class = BlogContextForm
    model = BlogContext
    template_name = "blog/create_blog.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点

    def form_valid(self, form):  # 设置外键的值，将目前用户和发的blog关联起来
        self.object = form.save(commit=False)
        self.object.modify_time = timezone.now()
        self.object.save()
        return super().form_valid(form)
        # form.instance.modify_time = timezone.now()


class DeleteBlog(LoginRequiredMixin, generic.DeleteView):
    model = BlogContext
    template_name = "blog/delete_confirm.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点
    success_url = reverse_lazy('home_page')  # 使用reverse_lazy可以保证在确认删除后才跳转到该域名


class DraftBlog(LoginRequiredMixin, generic.ListView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    model = BlogContext
    template_name = "blog/draft_list.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点
    def get_queryset(self):
        return BlogContext.objects.filter(publish_time__isnull=True, publisher__exact=self.request.user.pk).order_by('-create_time')


@login_required
def add_comment(request, pk):
    blog = get_object_or_404(BlogContext, pk=pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publisher = request.user
            comment.relatedblog = blog
            comment.save()
            return redirect('blog_content', pk=blog.pk)
    else:
        form = CommentsForm()
    return render(request, 'blog/comment.html', {'form': form})


@login_required
def approve_comment(request, pk):
    blog = get_object_or_404(BlogContext, pk=pk)
    blog.approve()
    return redirect('blog_content', pk=blog.pk)


@login_required
def notapprove_comment(request, pk):
    blog = get_object_or_404(BlogContext, pk=pk)
    blog.notapprove()
    return redirect('blog_content', pk=blog.pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    blog_pk = comment.relatedblog.pk
    comment.delete()
    return redirect('blog_content', pk=blog_pk)


@login_required
def publish_blog(request, pk):
    blog = get_object_or_404(BlogContext, pk=pk)
    blog.publish()
    return redirect('blog_content', pk=pk)


@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    published_blogs = BlogContext.objects.filter(publisher__exact=pk, publish_time__isnull=False).order_by('-create_time')
    created_blogs = BlogContext.objects.filter(publisher__exact=pk, publish_time__isnull=True).order_by('-create_time')
    return render(request, 'blog/profile.html', {'user': user, 'published_blogs': published_blogs, 'created_blogs': created_blogs})


def register(request):
    registered = False
    pwd_error = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():  # 检查两个form是否正确
            user = user_form.save()  # 将用户信息保存
            # user.set_password(user.password1)  # 将密码转为Hash值提高安全性
            user.save()  # 更新hash后的密码并保存
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)  # 将用户头像保存
            profile.user = user  # 设置one-to-one关系
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()  # 保存头像信息
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)
    else:
        # 用户没有填写信息
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'authorization/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'pwd_error': pwd_error})
