from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.


def es_admin(user: User):
    # Retorna True si el usuario pertenece al grupo 'Administrador'
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

# View for the login page
def login_view(request):
    # Revisamos si el usuario ya esta logueado. Si es asi, lo mandamos directo al dashboard
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        # Obtenemos los datos del formulario
        email_recibido = request.POST.get('email')
        password_recibido = request.POST.get('password')

        try:
            # Buscar al usuario con ese correo
            usuario_encontrado = User.objects.get(email=email_recibido)
            # Verfificamos la contrasena
            user = authenticate(request, username=usuario_encontrado.username, password=password_recibido)

            if user is not None: # Si existe
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Contrasena incorrecta.")

        except User.DoesNotExist:
            # Si el correo no existe en la base de datos
            messages.error(request, "No existe un usuario con ese correo.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request) # Se borra la sesion
    return redirect('login')

# Vista de la tabla de usuarios. Solo debe ser vista por los administradores
@login_required
@user_passes_test(es_admin)
def admin_table_view(request):
    return render(request, 'admin_table.html')

# Vista del index, debe estar logueado
@login_required
def index_view(request):
    return render(request, 'index.html')

@login_required
def patients_view(request):
    return render(request, 'tabla_pacientes.html')