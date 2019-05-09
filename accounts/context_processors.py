


from .forms import RegisterForm

def register_form(request):
    return {
     'register_form' : RegisterForm()
}