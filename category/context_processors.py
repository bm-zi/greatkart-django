from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
    
    # dict(links=links)
    # Creates a dictionary with key/value equal to links/links 
    # {links:links,} 
