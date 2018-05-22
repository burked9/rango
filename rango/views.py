from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request): #1
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def about(request): #2
    context_dict = {'boldmessage': "I am bold font from the context - New_view Excercise 5.6"}
    return render(request, 'rango/about.html', context_dict)

@login_required
def add_category(request): #3
    if request.method == 'POST': 
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)   
        else:
            print (form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form}) 

def category(request, category_name_slug): #4
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:   # We get here if we didn't find the specified category.
        pass  # Don't do anything - the template displays the "no category" message for us.
    return render(request, 'rango/category.html', context_dict) 

@login_required
def add_page(request, category_name_slug): #5
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None
    if request.method == 'POST': 
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)  # probably better to use a redirect here.
        else:    
            print (form.errors)
    else:
        form = PageForm()
    context_dict = {'form':form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)

def register(request): #6
    registered = False # A boolean value to set the initial status to False until registration is sucessful.
    if request.method == 'POST': #Only process if it's a HTTP Post.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Save the users form data    
            user.set_password(user.password) # Hash the password with set_password and update user object.
            user.save
            profile = profile_form.save(commit=False) # As we set the user ourselves we set commit to False, and we delay saving the model for now.
            profile.user = user
            if 'picture' in request.FILES: #If the user provided a pic get it from the input form and put it in the UserProfile Model.
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True # Update variable to tell the template the registration was sucessful.    
        else: # Invalid forms, mistakes or anything else will show up in the terminal.
            print (user_form.errors, profile_form.errors)
    else: # Not a HTTP Post so we render ModelForm Instances which will be blank and ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request): #7
    if request.method == 'POST': #Only process if it's a HTTP Post.
        username = request.POST.get('username') # This information is obtained from the login form.
        password = request.POST.get('password') # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'], # because the request.POST.get('<variable>') returns None, if the value does not exist,
                                                # while the request.POST['<variable>'] will raise key error exception
        user = authenticate(username=username, password=password) # Use Djangos machinery to validate the combination.    
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else: # An inactive account was used so no logging in
                return HttpResponse("Your Rango Account is disabled")
        else: #Bad login details were provided so we can't login
            print ("Invalid login details: {0}. {1}".format(username, password))
            return HttpResponse("Invalid login details supplied")

    # The request is not a HTTP POST, so display the login form.    # This scenario would most likely be a HTTP GET.
    else: # No context variables to pass to the template system, hence the blank dictionary object...
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request): #8
    logout(request)
    return HttpResponseRedirect('/rango/')

@login_required
def restricted(request): #9 -- Maybe be just a text test
    return HttpResponse("Since you're logged in, you can see this text!")

'''
def page(request, page_title): ## cancelled attempt at an excercise.
    context_dict = {}
    try:
        page = Page.objects.get(title=page_title)
        context_dict['page_title'] = page.title
    except Page.DoesNotExist:
        print('View Error')
        pass
    return render(request, 'rango/page.html', context_dict)     
'''        