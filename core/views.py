from django.shortcuts import render

# Create your views here.
# View for the login page
def login_view(request):
    return render(request, 'login.html')

# View for the admin table page
def admin_table_view(request):
    return render(request, 'admin_table.html')

def index_view(request):
    return render(request, 'index.html')