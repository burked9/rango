from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    page_list = Page.objects.order_by('-views')[:5]
    

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'boldmessage': "I am bold font from the context - New_view Excercise 5.6"}
    return render(request, 'rango/about.html', context_dict)

def add_category(request):
    if request.method == 'POST': #Is it a HTTP POST?
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            form.save(commit=True)
            #Now call the index() view & the user will be shown the homepage.
            return index(request)
        else:
            print (form.errors)
    else:
        form = CategoryForm()
    
    return render(request, 'rango/add_category.html', {'form': form}) ## Bad form or form details, render the form with error messages if any.

def category(request, category_name_slug):

    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        #context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict) 

def page(request, page_title):
    context_dict = {}
    try:
        page = Page.objects.get(title=page_title)
        context_dict['page_title'] = page.title
    except Page.DoesNotExist:
        print('View Error')
        pass
    return render(request, 'rango/page.html', context_dict)     

def add_page(request, category_name_slug):

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