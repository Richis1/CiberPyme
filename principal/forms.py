from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Intentar autenticar normalmente
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            if self.user_cache is None:
                # Comprobar si el usuario existe y si la contraseña es correcta pero está inactivo
                try:
                    user = User.objects.get(username=username)
                    if user.check_password(password):
                        if not user.is_active:
                            raise ValidationError(
                                "El usuario está desactivado.",
                                code='inactive',
                            )
                except User.DoesNotExist:
                    pass
                
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
