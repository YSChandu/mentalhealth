from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db import connection
from transformers import pipeline, Conversation  # Import Conversation from transformers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Conversation as UserConversation  # Ensure this model is defined properly in your models.py

from transformers import pipeline, Conversation

chatbot = pipeline("conversational", model="gpt2")

def get_chatbot_response(user_input):
    # Create a conversation prompt with a focus on mental health and supportive responses
    prompt = (f"The user says: '{user_input}'. Please provide an empathetic response that includes mental health tips, "
              "practical advice, and suggestions for improving well-being. Ensure the response is supportive, "
              "encouraging, and helpful for the user's emotional state.")

    # Generate a response using the chatbot
    response = chatbot(prompt,num_return_sequences=1, temperature=0.7)
    
    # Return the generated response as a string
    return response[0]['generated_text'].strip()


@login_required
def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        bot_response = get_chatbot_response(user_input)

        # Save the conversation to the database for the logged-in user
        conversation = UserConversation(user=request.user, user_input=user_input, bot_response=bot_response)
        conversation.save()

        # Fetch the user's previous conversations to display them
        user_conversations = UserConversation.objects.filter(user=request.user).order_by('-timestamp')

        return render(request, 'chatbot.html', {
            'bot_response': bot_response,
            'user_input': user_input,
            'conversations': user_conversations
        })

    # If no POST request, just display previous conversations
    user_conversations = UserConversation.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chatbot.html', {'conversations': user_conversations})


def home(request):
    return render(request ,'home.html')

def my_profile(request):
    user = request.user 
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_profile;")
        rows = cursor.fetchall()
        
    results = [{'1': row[0], '2': row[2], '3': row[3] , '4':row[4]} for row in rows]
    context = {
        'user': user,
        'result':results
    }
    
    return render(request, 'myprofile.html', context)


def register(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username is already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email is already exists")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                user.save();
                return redirect('login')
            
        else:
            messages.info(request,"passwords are not the same")
            return redirect('register')
    else:
        return render(request,'register.html')
    
    
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
        
    else:
       return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def resources(request):
    return render(request ,'resources.html')

def yoga(request):
    return render(request,'yoga.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def edit_profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

def issues(request):
    return render(request,'issues.html')

def anxietyissue(request):
    return render(request,'anxiety_issue.html')

def music(request):
    return render(request,"music.html")