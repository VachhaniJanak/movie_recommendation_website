from django import forms


class Register(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        label='username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name',
            }
        ),
        error_messages={
            "required": "Please enter your name"
        }
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        label='email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        ),
        error_messages={
            "required": "Please enter your email"
        }
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        ),
        error_messages={
            "required": "Please enter password"
        }
    )

    conform_password = forms.CharField(
        max_length=100,
        required=True,
        label='conform_password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Conform Password',
            }
        ),
        error_messages={
            "required": "Please enter password"
        }
    )


class Login(forms.Form):
    email = forms.EmailField(
        max_length=50,
        required=True,
        label='email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        ),
        error_messages={
            "required": "Please enter your email"
        }
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        ),
        error_messages={
            "required": "Please enter password"
        }
    )


class EmailVerification(forms.Form):
    email = forms.EmailField(
        max_length=50,
        required=True,
        label='email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        ),
        error_messages={
            "required": "Please enter your email"
        }
    )


class PasswordReset(forms.Form):
    code = forms.CharField(
        max_length=6,
        required=True,
        label='code',
        widget=forms.TextInput(
            attrs={
                'placeholder': '6-Digit Code',
            }
        ),
        error_messages={
            "required": "Enter 6-digit code sent to your mail"
        }
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Set new Password',
            }
        ),
        error_messages={
            "required": "Please enter password"
        }
    )

    conform_password = forms.CharField(
        max_length=100,
        required=True,
        label='conform_password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Conform Password',
            }
        ),
        error_messages={
            "required": "Please enter password"
        }
    )