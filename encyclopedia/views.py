from django.shortcuts import render
from . import util

from markdown import markdown 

import logging
from click import secho
from django import forms
import random

class NewPage(forms.Form):
    title    = forms.CharField( label="title" ) # We are going to use the label to access the title
    textarea = forms.CharField( widget=forms.Textarea )

class Search(forms.Form):
    query = forms.CharField( label="query" )

def index(request):
    secho( "[DEBUG] --> CURRENTLY AT INDEX\n\n", fg="green" )
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry( request, title ):
    
    page = util.get_entry( title )
    
    if not page:
        return render( request, "encyclopedia/404.html" )
    
    return render( request, "encyclopedia/pages.html" , {
        "title" : title.upper(),
        "content" : markdown( page ),
    } )


def create_page( request ):
    if request.method == "POST":
        secho( "<<<<<<<A post message was submitted>>>>>>>", fg="green" )
        new_page = NewPage( request.POST ) # I think we will have to stick with naming this variable form
        
        if new_page.is_valid():
            title    = new_page.cleaned_data[ "title" ]
            textarea = new_page.cleaned_data[ "textarea" ] 

            # DEBUG
            secho( f"Request has title -> { title }", fg="green" )
            secho( f"Request has body -> \n{ textarea }", fg="green" )
            
            for page in util.list_entries():
                if page.lower() == title.lower():
                    return render( request, "encyclopedia/page_exists.html" )
            
            util.save_entry( title,"# " + title + "\n" + textarea )
            return render( request, "encyclopedia/index.html" )
            
    return render( request, "encyclopedia/create_page.html", {
        "form" : NewPage(),
    } )


def search( request ):
    """
    This is for when the user submits a search
    """
    secho( "[DEBUG] --> search function triggered", fg="green" )
    if request.method == "POST":
        
        query = request.POST['q']

        if not query: return render( request, "encyclopedia/404.html" )

        q = query
        all_entries = util.list_entries()

        found = [ entry for entry in all_entries if q.lower() in entry.lower() ]
        secho(found, fg="yellow")
        if not found: 
            return render( request, "encyclopedia/pages.html", {
                "title"   : "PAGE NOT FOUND",
                "content" : f"<h1> PAGE NOT FOUND </h1>\
                              <h3> {q.upper()} not available in this encyclopedia"
            } )

        if len(found) == 1 :
            return render( request, "encyclopedia/pages.html", {
                        "title"   : q.upper(),
                        "content" : markdown( util.get_entry( found[0] ) ),
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                        "entries": found
                    })


def random_page( request ):
    
    page_to_render = random.choice( util.list_entries() )
    
    return render( request, "encyclopedia/pages.html", {
        "title"   : page_to_render.upper(),
        "content" : markdown( util.get_entry( page_to_render ) ),
        })