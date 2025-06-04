from django.shortcuts import render
from . import util

from markdown import markdown 

import logging
from click import secho

def index(request):
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
    logger = logging.getLogger(__name__)
    if request.method == "POST":
        logger.info( "This works" )
        secho( "This works", fg="green" )
        
    return render( request, "encyclopedia/create_page.html" )

