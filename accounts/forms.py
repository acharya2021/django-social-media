# imports the user model active in this project
from django.contrib.auth import get_user_model

# there is a user creation form built into the authorization package
# this is essentially gonna be a signup page
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        # these fields are already available from contrib.auth
        # comes with the authorization model to confirm your password
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # optional, for labels on the signup form
            self.fields["username"].label = "Display Name"
            self.fields["email"].label = "Email Address"
