import markdown2
import random
import re
from django.shortcuts import render, redirect, HttpResponse

from . import util

# global variable

pagelist = util.list_entries()

# default page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    #entra a util y entra a la funcion "list_entries" que genera un lista de la entries
    pagelist = util.list_entries()
    if title in pagelist:
        content = util.get_entry(title)

        return render(request, "encyclopedia/page.html", {
        "title": title,
        #"key of content(variable of name)":argument.method
        "content": markdown2.markdown(content)
                # send title and content to HTML
        })
    else:
        return render(request, "encyclopedia/error.html", {
            'error_message': 'Page not found'
        })

# random page

def random_page(request):
    # if there is no -1, it could get until 5. And there is no element in the number 5.
    # random no. from 0 to 4
    r = random.randint(0,len(pagelist)-1)
    print (r)
    # Depending on the number, it will give a element of the list
    title = pagelist[r]
    # redirect(what url want to go, name of the url)
    # path("wiki/<str:title>", views.wiki, name="wiki")
    return redirect(wiki, title=title)

# Search

def search(request):
    #If the user send a form, it must be an POST method
    if request.method == "POST":
        # the variable is q and the value would be what the user type
        term = request.POST['q']
        print(term)
        searchlist = []
        # pagelist = ['CSS', 'Django', 'Git', 'HTML', 'Markdown', 'Python', 'Test']
        for page in pagelist:
            # re.search(lo que buscas, con lo que que tienes)
            if re.match(term.lower(), page.lower()):
                # the word is appended to the list
                searchlist.append(page)
                print(searchlist)
            # if the list is empty
        if len(searchlist) == 0:
                # send the request to error.html and post that message
                return render(request, "encyclopedia/error.html", {
                    'error_message': f'No results found for \'{term}\''
                })
    # Send the searchlist to search.html
    return render (request, "encyclopedia/search.html", {
        'entries': searchlist
    })


def add_page(request):
    # It checks
    if request.method == 'POST':
        # Save the data from the forms in title and content variables 
        title = request.POST.get('title')
        content = request.POST.get('content')

        # if there is a dm with the same title send TRUE
        if title in pagelist:
            return render(request, "encyclopedia/add.html",{
                'available': True
            })
        else:
            # Enter to util.py // function save_entry
            util.save_entry(title, content)
            return redirect(wiki, title=title)

    return render(request, "encyclopedia/add.html",{
        'available': False
    })
