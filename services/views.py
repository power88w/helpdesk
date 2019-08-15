from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import BlogPost,BlogComment,BlogStats
from django.core.paginator import Paginator
from services.models import BlogPost as fbp
from cart.models import session
from django.db import IntegrityError

################# DETAIL Blog##############

def Blog_Post_Detail_Page(request,post_id):
    obj =  get_object_or_404(BlogPost, id=post_id)
    com_obj = BlogComment.objects.filter(Blog=obj)
    paginator = Paginator(com_obj, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    template_name='services-detail.html'
    ## view ###
    if not request.user.is_anonymous:
        query_visit=BlogStats.objects.filter(blog=obj,user=request.user)
        if query_visit.count()==0:
            obj.views+=1
            obj.save()
            BlogStats(blog=obj,user=request.user,views=1).save()
    context={"Blog":obj,"title":"Detail","comments":comments}
    return render(request,template_name,context)

################# CREATE BLOG ##############
@login_required(login_url='/login/accounts/login')
def Blog_Post_Create_Page(request):
    if request.POST or request.FILES:
        title = request.POST.get('title')
        content = request.POST.get('content')
        pr = request.POST.get('priority')
        if request.FILES:
            image = request.FILES['image']
            # save ima
            # s3.upload_file(image.read(), BUCKET, image.name)
            # fs = FileSystemStorage()
            # mi = fs.save(image.name, image)
            BlogPost(title=title,priority=pr,content=content,images=image,user=request.user).save()
        else:
            BlogPost(user=request.user,title=title,priority=pr,content=content).save()
        return redirect('/services/')
    template_name="create.html"
    context = {}
    return render(request,template_name,context)

#################  LIST BLOG ################

def Blog_Post_List_Page(request):
    objs = BlogPost.objects.order_by('posted_time')[::-1]
    paginator = Paginator(objs, 5)
    template_name="services.html"
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {"objects":blogs}
    return render(request,template_name,context)

##############  New Comment  ##########
@login_required(login_url='/login/accounts/login')
def Create_Comment(request,post_id):
    if request.POST:
        newComment = BlogComment(user = request.user, Comment = request.POST['comment'],
                                    Blog_id=post_id)
        newComment.save()
        return redirect("/services/"+post_id+"/")
    template_name = "blog/create_comment.html"
    context={}
    return render(request,template_name,context)

###############  Edit Comment #########
@login_required(login_url='/login/accounts/login')
def Edit_Comment(request,comment_id):
    comment = get_object_or_404(BlogComment,id= comment_id)
    blog = comment.Blog
    if request.POST:
        comment.Comment = request.POST["edited_comment"]
        comment.save()
        return redirect("/services/"+str(blog.slug)+"/")
    template_name = "blog/edit_comment.html"
    context = {"comment_to_edit":comment.Comment}
    return render(request,template_name,context)

############## Comment Delete ###############
@login_required(login_url='/login/accounts/login')
def Delete_Comment(request,comment_id):
    comment = get_object_or_404(BlogComment,id= comment_id)
    blog = comment.Blog
    if request.POST:
        comment.delete()
        return redirect("/services/"+str(blog.slug)+"/")
    template_name = "blog/delete_comment.html"
    return render(request,template_name)


############# BLOG UPVOTE ###############
@login_required(login_url='/login/accounts/login')
def  Blog_Like(request,post_id):
    from_blog=get_object_or_404(BlogPost,id=post_id)
    a=get_object_or_404(BlogStats,blog=from_blog,user=request.user)
    if a.rating==1:
        from_blog.votes -=1
        from_blog.save()
        a.rating =0
        a.save()
    elif a.rating==0:
        from_blog.votes +=1
        from_blog.save()
        a.rating =1
        a.save()
    return redirect("/services/"+str(from_blog.id)+"/")


############# Donate ############
@login_required(login_url='/login/accounts/login')
def Donate(request):
    template = "blog/donate.html"
    prev=0
    if request.POST:
        try:
            a=fbp.objects.create(title="donate")
            session.objects.create(user=request.user, name=a,rate=request.POST.get("money"))
            return redirect("/cart/")
        except IntegrityError:
            a=fbp.objects.get(title="donate")
            prev=a.value
            a.delete()
            a=fbp.objects.create(title="donate")
            session.objects.create(user=request.user, name=a,rate=request.POST.get("money"))
            return redirect("/cart/")
    context = {"pre_val":prev}
    return render(request,template,context)