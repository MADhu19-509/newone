from email import message
from symbol import decorator
from django.shortcuts import render,redirect
from django.contrib import messages
from django import shortcuts
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from itertools import chain
import random
from .models import followerscount, profile,posts,likes,followerscount
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(user=request.user.username)
    user_profile= profile.objects.get(user=user_object)

    user_following_list=[]
    post_feed=[]
    user_following= followerscount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = posts.objects.filter(user=usernames)
        post_feed.append(feed_lists)

        feed_list =list(chain(*post_feed))
        
        #user suggestion starts here
        all_users=User.objects.all()
        user_following_all=[]

        for user in user_following:
            user_list=User.objects.get(username=user.user)
            user_following_all.append(user_list)
            
        new_suggestion_list=[x for x in list(all_users)if (x not in list(user_following_all))]
        current_user=User.objects.filter(username=request.user.username)
        final_suggestion_list= [x for x in list(new_suggestion_list) if (x not in list(current_user))]
        random.shuffle(final_suggestion_list)

        username_profile=[]
        username_profile_list=[]
        for users in final_suggestion_list:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_list=profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)
        
        suggestion_username_profile_list=list(chain(*username_profile_list))

    return render(request,'index.html',{'user_profile':user_profile,'post_feed':post_feed,'suggestion_username_profile_list':suggestion_username_profile_list[:4]})


def signin(request):
    if  request.method == "POST":
        username=request.POST['username']
        password= request.POST['password']

        user=auth.authenticate(username=username,password=password)
        
        if user is None:
            messages.info(request,"credential invalid")
            return redirect("signin")
        else :
            auth.login(request,user)
            return redirect('/')


    else:
        return render(request,'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')

def signup(request): 
        if request.method =='POST':
            password= request.POST['password']
            password2= request.POST['password2']
            username=request.POST['username']
            email=request.POST['email']
            
       

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'email already exists')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request,'username taken')
                    return redirect('signup')
            else:
                user =User.objects.create_user(username=username,email=email,password=password2)
                user.save() 
                messages.info('request','signed up succesfully  ')
                #login user  and redirecting to settings 
                user_login=auth.authenticate(username=username,password=password )
                auth.login(request,user)

                
                # creating a profile for the user

                user_model = User.objects.get(username=username)
                new_profile = profile.objects.create(user=user_model,id =user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            return render(request,'signup.html')

@login_required(login_url='signin')
def settings(request):
    user_profile =profile.objects.get(user=request.user)
    if request.method=='POST':
        if request.FILES.get('image')== None:
            image=user_profile.prof_img
            bio =request.POST['bio']
            location =request.POST['location']

            user_profile.prof_img=image
            user_profile.bio=bio
            user_profile,location= location
            user_profile.save()

        if request.FILES.get('image') != None:
            image=request.FILES.get['image']
            bio =request.POST['bio']
            location =request.POST['location']

            user_profile.prof_img=image
            user_profile.bio=bio
            user_profile.location= location
            user_profile.save()

    return render(request,'setting.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=posts.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect("/")
    else:
        return redirect("/")

    return HttpResponse('<h2>upload views</h2>')

@login_required(login_url='signin')
def likes(request):
    username =request.user.username
    post_id=request.GET.get('post_id')

    Post=posts.objects.get(id=post_id)

    like_filter=likes.objects.filter(post_id=post_id, username=username).first
    
    
    if like_filter == None:
        new_like=likes.objects.create(post_id=post_id,username =username )
        new_like.save()
        posts.no_of_likes= posts.no_of_likes+1
        posts.save()
        return redirect('/')
    else:
        like_filter.delete()
        posts.no_of_likes= posts.no_of_likes-1
        posts.save()
        return redirect("/")

@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=profile.objects.get(user=user_object)
    user_post=posts.ojects.filter(user=pk)
    user_post_length=len(user_post)
    
    follower =request.user.username
    user=pk 
    if followerscount.objects.filter(follower=follower,user=user).first():
        button_text='unfollow'
    else:
        button_text='follow'
    
    user_followers=len(followerscount.objects.filter(user=pk))
    user_following=len(followerscount.objects.filter(follower=pk))

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_length':user_post_length,
        'user_followers':user_followers,
        'user_following':user_following,
        

            }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['user']

        if followerscount.objects.filter(follower=follower,user=user).first():
           del_follower=followerscount.objects(follower=follower,user=user) 
           del_follower.delete() 
           return redirect("/profile/"+user)
        else:
            new_follower=followerscount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else :
        return redirect("/")

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(user=user_object)

    if request.method=='POST':
        username=request.post['username']
        username_object=User.object.filter(username__icontain=username)

        username_profile=[]
        username_profile_list=[]
        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists=profile.objects.filter(id_users=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list=list(chain(*username_profile_list))

    return render(request,'search.html',{' user_profile': user_profile,'username_profile_list':username_profile_list})





   
    