from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Feature
import joblib
from transformers import pipeline

# model_path = "./text_generator.h4"
# text_generator = joblib.load(model_path)
# classifier = pipeline('sentiment-analysis')

# generator = pipeline('text-generation', model='gpt2')

# def submit(request):
#     generated_text = ""
#     if request.method == "POST":
#         user_input = request.POST.get('input_text')
#         if user_input:
#             result = classifier(user_input)
#             generated_text_dict = generator(user_input, max_length=500, num_return_sequences=1, truncation=True)
#             generated_text = generated_text_dict[0]['generated_text']
#             generated_text = generated_text.encode('ascii', 'ignore').decode('utf-8')
#         else:
#             generated_text = "Please enter valid text."
#     context={'generated_text': generated_text,"result":result}
#     return render(request, 'generator.html', context)

    
def home(request):
    features=Feature.objects.all()
    return render(request ,'home.html',{'features':features})
def register(request):
    if request.method =='POST':
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
                user=User.objects.create_user(username=username,email=email,password=password)
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