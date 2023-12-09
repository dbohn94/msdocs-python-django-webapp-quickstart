from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#Index view: URL Endpoint index, HTTP method (GET by default)
#Behavior: prints a message to the console indicating that a request for the index page has been recieved and then renders an HTML template named 'hello_azure/index.html' using the render function.
#The rendered HTML is then sent as the HTTP response 
def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

#hello view: handles both GET and POST requests 
#Behavior: POST, retrieves the value of the 'name' parameter from the POST data
@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')