import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Doctor, Patient, Appointment, WellnessTransaction
import re
import io
import base64
import matplotlib.pyplot as plt
from django.conf import settings
from django.http import JsonResponse
import google.generativeai as ai
from django.db.models import Q

# Helper function to load API key
def load_api_key():
    try:
        with open('config.json') as f:
            config = json.load(f)
            return config.get('API_KEY')
    except FileNotFoundError:
        print("Error: config.json file not found.")
        return None

# # Registration View

# from django.core.exceptions import ValidationError
# from django.core.validators import EmailValidator
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.shortcuts import render, redirect

# User = get_user_model()

# def check_password_strength(password):
#     # Implement your password strength checking logic here
#     # Example: Ensure password is at least 8 characters long, contains upper/lowercase letters, etc.
#     if len(password) < 8:
#         return False, "Password must be at least 8 characters long."
#     if not any(char.isdigit() for char in password):
#         return False, "Password must contain at least one number."
#     if not any(char.islower() for char in password):
#         return False, "Password must contain at least one lowercase letter."
#     if not any(char.isupper() for char in password):
#         return False, "Password must contain at least one uppercase letter."
#     if not any(char in '!@#$%^&*()_+' for char in password):
#         return False, "Password must contain at least one special character."
#     return True, ""


# def registration(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']

#         # Check if passwords match
#         if password != cpassword:
#             messages.error(request, "Passwords do not match.")
#         else:
#             # Check for existing email or username
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "An account with this email already exists.")
#             elif User.objects.filter(username=username).exists():
#                 messages.error(request, "Username already taken.")
#             else:
#                 # Email validation
#                 try:
#                     validator = EmailValidator()
#                     validator(email)  # Will raise ValidationError if invalid
#                 except ValidationError:
#                     messages.error(request, "Invalid email format. Please enter a valid email address.")
#                 else:
#                     # Check password strength
#                     is_valid, error_message = check_password_strength(password)
#                     if not is_valid:
#                         messages.error(request, error_message)
#                     else:
#                         # Create user if email is valid and password is strong
#                         User.objects.create_user(username=username, email=email, password=password)
#                         messages.success(request, "Registration successful! You can now log in.")
#                         return redirect('login')  # Redirect to login page

#     return render(request, 'registration.html')




# @csrf_protect
# def registration(request):
#     if request.method == "POST":
#         # Get data from POST request
#         us = request.POST.get('username')
#         em = request.POST.get('email')
#         ps = request.POST.get('password')
#         cps = request.POST.get('cpassword')

#         # Check if passwords match
#         if ps != cps:
#             return render(request, 'registration.html', {'error': 'Passwords do not match!'})

#         # Check if the username already exists
#         if User.objects.filter(username=us).exists():
#             return render(request, 'registration.html', {'error': 'Username already exists!'})

#         try:
#             # Create and save a new user
#             user = User.objects.create_user(username=us, email=em, password=ps)
#             user.save()

#             # Redirect to login page after successful registration
#             return redirect('login')

#         except Exception as e:
#             # Handle any error that might occur
#             print(f"Error: {e}")
#             return render(request, 'registration.html', {'error': 'An error occurred while creating the user.'})

#     return render(request, 'registration.html')


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
import re


def is_strong_password(password):
    """
    Validate password strength.
    - Must be at least 8 characters long
    - Must contain at least one uppercase letter
    - Must contain at least one lowercase letter
    - Must contain at least one digit
    - Must contain at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",<>\./?]', password):
        return False, "Password must contain at least one special character."
    return True, ""


@csrf_protect
def registration(request):
    if request.method == "POST":
        # Get data from POST request
        us = request.POST.get('username')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cps = request.POST.get('cpassword')

        # Check if passwords match
        if ps != cps:
            return render(request, 'registration.html', {'error': 'Passwords do not match!'})

        # Check if the email is valid
        try:
            EmailValidator()(em)  # Raises ValidationError if the email is invalid
        except ValidationError:
            return render(request, 'registration.html', {'error': 'Invalid email format. Please enter a valid email address.'})

        # Check if the username or email already exists
        if User.objects.filter(username=us).exists():
            return render(request, 'registration.html', {'error': 'Username already exists!'})
        if User.objects.filter(email=em).exists():
            return render(request, 'registration.html', {'error': 'An account with this email already exists!'})

        # Check password strength
        is_valid, error_message = is_strong_password(ps)
        if not is_valid:
            return render(request, 'registration.html', {'error': error_message})

        try:
            # Create and save a new user
            user = User.objects.create_user(username=us, email=em, password=ps)
            user.save()

            # Redirect to login page after successful registration
            return redirect('login')

        except Exception as e:
            # Handle any error that might occur
            print(f"Error: {e}")
            return render(request, 'registration.html', {'error': 'An error occurred while creating the user.'})

    return render(request, 'registration.html')










@csrf_protect
def login(request):
    if request.method == "POST":
        # Get username and password from the form
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, "Login successful!")
            # Redirect to the success page
            return redirect('home')  # Make sure to create a success URL
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

# Logout View
def logout(request):
   
    auth_logout(request)  # Use Django's built-in logout function
    messages.success(request, "Logged out successfully.")
    return redirect('home')



# Home View
def home(request):
    return render(request, 'home.html',{'is_authenticated': request.user.is_authenticated})


# Dashboard View
def dashboard(request):
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'recent_doctors': Doctor.objects.all().order_by('-id')[:3],
        'recent_patients': Patient.objects.all().order_by('-id')[:3],
        'recent_appointments': Appointment.objects.all().order_by('-appointment_date')[:3],
    }
    return render(request, 'dashboard.html', context)


# Wellness Tracking View
def wellnesstracking(request):
    search_query = request.GET.get('search', '')
    transactions = (
        WellnessTransaction.objects.filter(
            Q(category_icontains=search_query) | Q(description_icontains=search_query)
        )
        if search_query
        else WellnessTransaction.objects.all()
    )
    return render(request, 'wellnesstracking.html', {'transactions': transactions, 'search_query': search_query})


def generate_comparison_graph(data, metric_name, normal_range):
    categories = ["Given", "Normal Range"]
    values = [data, normal_range]
    
    # Create figure for the chart
    plt.figure(figsize=(6, 4))
    plt.bar(categories, values, color=["orange", "green"])
    plt.title(f"{metric_name} Comparison")
    plt.ylabel(metric_name)
    
    # Save plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    
    # Encode to base64
    graph_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return graph_base64

# Function to get recommendation from Google Gemini AI
def get_gemini_ai_recommendation(health_data):
    api_key = load_api_key()
    
    if not api_key:
        return {"error": "API key not found."}
    
    ai.configure(api_key=api_key)
    model = ai.GenerativeModel("gemini-pro")
    chat = model.start_chat()

    # AI prompt for generating health recommendations
    prompt = (f"Based on the following health data, give recommendations if they are not in good health range \n"
              f"Heart Rate: {health_data.get('heart_rate')}\n"
              f"Sleep Hours: {health_data.get('sleep_hours')}\n"
              f"Steps: {health_data.get('steps')}\n"
              f"Calories Burnt: {health_data.get('calories_burnt')}")
    
    try:
        # Send the prompt to the AI model for health recommendations
        response = chat.send_message(prompt)
        recommendations = response.text.strip()

        # Split the response into bullet points
        points = recommendations.split("\n")
        points = [point.strip() for point in points if point.strip() != ""]
        short_points = points[:10]  # Limit to 5-10 points
        bullet_points = [f"• {point}" for point in short_points]
        
        return bullet_points

    except Exception as e:
        return {"error": str(e)}

def healthinsights(request):
    if request.method == "POST":
        # Collect health data from POST request
        heart_rate = float(request.POST.get("heart_rate", 70))
        sleep_hours = float(request.POST.get("sleep_hours", 8))
        steps = int(request.POST.get("steps", 10000))
        calories_burnt = float(request.POST.get("calories_burnt", 250))

        # Normal ranges
        heart_rate_normal = 77  # Normal range for heart rate (bpm)
        sleep_normal = 9  # Normal range for sleep hours
        steps_normal = 10000  # Normal range for steps
        calories_burnt_normal = 3000  # Normal range for calories burnt

        # Generate graphs for each metric
        heart_rate_graph = generate_comparison_graph(heart_rate, "Heart Rate (bpm)", heart_rate_normal)
        sleep_graph = generate_comparison_graph(sleep_hours, "Sleep Hours (hours)", sleep_normal)
        steps_graph = generate_comparison_graph(steps, "Steps", steps_normal)
        calories_graph = generate_comparison_graph(calories_burnt, "Calories Burnt (kcal)", calories_burnt_normal)

        # Prepare health data for AI recommendation
        health_data = {
            "heart_rate": heart_rate,
            "sleep_hours": sleep_hours,
            "steps": steps,
            "calories_burnt": calories_burnt
        }

        # Get AI-generated recommendations
        ai_recommendation = get_gemini_ai_recommendation(health_data)

        # Return both graphs and AI response in the JSON response
        return JsonResponse({
            "heart_rate_graph": heart_rate_graph,
            "sleep_graph": sleep_graph,
            "steps_graph": steps_graph,
            "calories_graph": calories_graph,
            "recommendations": ai_recommendation
        })

    return render(request, "healthinsights.html")

def health_suggestions(request):
    api_key = load_api_key()
    
    if not api_key:
        return JsonResponse({"error": "API key not found."})
    
    ai.configure(api_key=api_key)
    model = ai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        
        # AI prompt for concise suggestions
        prompt = f"Provide 5-10 short points for home remedies or health advice for: {user_input}"

        try:
            response = chat.send_message(prompt)
            suggestions = response.text.strip()

            # Split the response into sentences or lines
            points = suggestions.split("\n")
            points = [point.strip() for point in points if point.strip() != ""]  # Clean up whitespace
            short_points = points[:10]  # Limit to 5-10 points

            # Format the suggestions into bullet points
            bullet_points = [f"{point}" for point in short_points]

            return JsonResponse({"suggestions": bullet_points})

        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    return render(request, "suggestions.html")



def suggest_medicine(request):
    # Add logic for suggesting medicine
    return render(request, 'suggest_medicine.html',{})