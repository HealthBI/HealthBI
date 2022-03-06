from django.shortcuts import render

# Create your views here.
def index(request):
    """View function for home page of site."""
    context = {
        'test': 1
        }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def upload_page(request):
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

def upload_csv(request):
    
    csv_file = request.FILES["csv_file"]

    file_data = csv_file.read().decode("utf-8")		

    lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
    for line in lines:						
        fields = line.split(",")
        data_dict = {}
        data_dict["Temporal"] = fields[0]
        data_dict["Location"] = fields[1]
        data_dict["Indicator1"] = fields[2]
        data_dict["Indicator2"] = fields[3]

        context = {
        'data': data_dict
        }

        return render(request, 'dictionaryMappings.html', context=context)