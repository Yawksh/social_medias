from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from  django.contrib import  messages
from .models import  Profile,Post,LikePost
from  django.contrib.auth.decorators import  login_required
from django.http import HttpResponse


# Create your views here. as much as needed
@login_required(login_url="signin")
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    posts = Post.objects.all().order_by('-created_at')
    return  render(request,'index.html',{"user_profile":user_profile,'posts':posts})
def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if password1==password2:
           # if the user already signuped with a given email address
           if User.objects.filter(email=email).exists():
               messages.info(request,"Email taken")
               return redirect("signup")
           elif User.objects.filter(username=username).exists():
               messages.info(request,"username taken already")
               return redirect("signup")
           else:
               user=User.objects.create_user(username=username,email=email,password=password1)
               user.save()#save user into database
               #log in user to setting page
               user_login=auth.authenticate(user,username=username,password=password1)
               auth.login(request,user_login)
               #create  a profile  object for new user
               user_model=User.objects.get(username=username)
                    # Create a profile object for the new user
               try:
                    
                    new_profile = Profile.objects.create(user=user_model, id_user=user.id)
                    new_profile.save()
                    messages.success(request, "User created successfully!")
                    return redirect("settings") 
                # Redirect to a success page or home
               except Exception as e:
                    messages.error(request, f"Error creating profile: {str(e)}")
            
        else:
            messages.error(request,"password not matching")
            return redirect("signup")


    else:
        return render(request,"signup.html")
def signin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.error(request,"credentials invalid")

    return render(request,'signin.html')

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")
@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        bio = request.POST.get('bio')
        location = request.POST.get("location")
        
        if request.FILES.get("image") is not None:
            image = request.FILES.get("image")
            user_profile.profile = image
        
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        # Redirect after saving changes
        messages.success(request, "Profile updated successfully!")
        return redirect("settings")

    return render(request, "setting.html", {"user_profile": user_profile})
def upload(request):
    if request.method=='POST':
      image = request.FILES.get('image_upload')
      if not image:
         return HttpResponse("No image uploaded!", status=400)

      user=request.user.username
      caption=request.POST.get("caption")

      new_post=Post.objects.create(user=user,image=image,caption=caption)
      new_post.save()
      return redirect('/')

    else:
        return redirect('/')


        
    return render("index.html")
@login_required(login_url="signin")
def like_post(request):
    username = request.user.username
    post_id = request.Get.get('post_id')
    post = Post.objects.filter(post_id = post_id)
