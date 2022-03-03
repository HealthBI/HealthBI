from django.shortcuts import render

# Create your views here.
def index(request):
    """View function for home page of site."""
    context = {
        'test': 1
        }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def upload(request):
    """View function for upload page."""
    context = {
        'test': 2
        }
    return render(request, 'upload.html', context=context)


def analysis(request):
    """View function for analysis page."""
    context = {
        'test': 3
        }
    return render(request, 'analysis.html', context=context)