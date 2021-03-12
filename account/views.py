from django.urls import reverse_lazy
from django.views import generic

from account.forms import SignUpForm


class RegisterView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'