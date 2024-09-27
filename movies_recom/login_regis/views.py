from random import sample
from typing import Any

from django.core.signals import request_finished
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.hashers import make_password


from celery import shared_task

from .form import Register, Login, PasswordReset, EmailVerification
from .models import UserInfo, UserSession

from_email = 'VWqB9@example.com'

@shared_task
def sendemail(email_to, subject, message):
	try:
		send_mail(subject=subject, message=message, from_email=from_email,recipient_list=[email_to])
	except Exception as e:
		print(e)


class RegisterView(View):
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(**kwargs)
		self.reg_form: Register
		self.data: dict
		self.user: UserInfo

		self.email_error: str = ""
		self.password_error: str = ""
		self.message: str = ""

	def get(self, request):
		self.reg_form = Register(request.GET)
		return self.redirect_reg(request=request)

	def post(self, request):
		self.reg_form = Register(request.POST)
		if self.reg_form.is_valid():
			self.data = self.reg_form.cleaned_data
			self.email_exists_create()
		return self.redirect_reg(request=request)

	def email_exists_create(self):
		if UserInfo.objects.filter(email=self.data.get('email')).exists():
			self.email_error = 'Email is already in use try to login'
		else:
			self.check_password()
			
	def check_password(self):
		if len(self.data.get('password')) > 8:
			self.both_matched()
		else:
			self.password_error = 'Password must be greater than 8 character'

	def both_matched(self):	
		if self.data.get('password') == self.data.get('conform_password'):
			UserInfo(username=self.data.get('username'),
						email=self.data.get('email').lower(),
						password=self.data.get('password')
					).save() 
			self.message = 'your account has been created successfully try to Login'
		else:
			self.message = 'Password not matched'

	def redirect_reg(self, request):
		return render(request, 'registration.html', {
			'reg_form': self.reg_form,
			'email_error': self.email_error,
			'message': self.message,
			'password_error': self.password_error
		})
		


class LoginView(View):
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(**kwargs)
		self.subject = 'Login Notification'
		self.message = 'Your account is recently login it\'s you.'
		self.max_num_login_device=3

		self.data: dict
		self.user: UserInfo
		self.loginform: Login
		
		self.email_error: str = ""
		self.password_error: str = ""

	def get(self, request):
		self.login_form = Login(request.GET)
		if UserInfo.objects.filter(id=request.session.get('id')).exists():
			return HttpResponseRedirect(reverse('home'))

		return self.redirect_login(request=request)
	
	def post(self, request):
		self.login_form = Login(request.POST)
		if self.login_form.is_valid():
			self.data = self.login_form.cleaned_data
			return self.emailexist(request=request)

		return self.redirect_login(request=request)

	def emailexist(self, request):
		self.user = UserInfo.objects.filter(email=self.data.get('email').lower()).first()
		if self.user:
			return self.password_iscorrect(request=request)
		
		self.email_error = 'Invalid Email'
		return self.redirect_login(request=request)
	
	def password_iscorrect(self, request):
		if check_password(self.data.get('password'), self.user.password):
			return self.multiple_login_found(request=request)
		
		self.password_error = 'Invalid Password'
		return self.redirect_login(request=request)
	
	def multiple_login_found(self, request):
		print(UserSession.objects.filter(user=self.user).count())
		if UserSession.objects.filter(user=self.user).count() < self.max_num_login_device:
			request.session['id'] = self.user.id
			self.store_user_session(request=request)			
			sendemail(email_to=self.user.email, subject=self.subject, message=self.message)
			return HttpResponseRedirect(reverse('home'))
		
		self.password_error = f'Login limit exceeded. \n Max Login device. {self.max_num_login_device}'	
		return self.redirect_login(request=request)

	def redirect_login(self, request):
		return render(request, 'login.html', {
				'login_form': self.login_form,
				'email_error': self.email_error,
				'password_error': self.password_error
			})
	
	def store_user_session(self, request):
		request.session.save()
		session_key = request.session.session_key
		# Check if the session_key already exists for this user
		if not UserSession.objects.filter(session_key=session_key).exists():
			UserSession.objects.create(user=self.user, session_key=session_key)



class EmailVerificationView(View):
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(**kwargs)
		self.code: str = ''.join(map(str, sample(range(10), 6)))

		self.subject='Forgot Password'
		self.email_message=f'Your code is {self.code}.\n Use this code' 
		
		self.email_verif_form: EmailVerification
		self.data: dict
		self.message: str = ""

	def get(self, request):
		self.email_verif_form = EmailVerification(request.GET)
		return self.redirect_verify(request=request)

	def post(self, request):
		self.email_verif_form = EmailVerification(request.POST)
		if self.email_verif_form.is_valid():
			self.data = self.email_verif_form.cleaned_data
			return self.email_exists(request=request)
		
		return self.redirect_verify(request=request)

	def email_exists(self, request):
		user = UserInfo.objects.filter(email=self.data.get('email').lower()).first()
		if user:
			sendemail(email_to=self.data.get('email'), subject=self.subject, message=self.email_message)
			request.session['id'] = user.id
			request.session['code'] = self.code
			self.store_user_session(request=request, user=user)
			print(request.session.get('code'), "="*128)
			return HttpResponseRedirect(reverse('forgot-password'))
		
		self.message = 'Invalid Email'
		return self.redirect_verify(request=request)

	def redirect_verify(self, request):
		return render(request, 'verifyemail.html', {
		'email_verif_form': self.email_verif_form,
		'message': self.message
	})

	def store_user_session(self, request, user):
		request.session.save()
		session_key = request.session.session_key
		# Check if the session_key already exists for this user
		if not UserSession.objects.filter(session_key=session_key).exists():
			UserSession.objects.create(user=user, session_key=session_key)

class PasswordResetView(View):
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(**kwargs)

		self.subject='Password Reset'
		self.message='your password has been reset successfully try to Login'

		self.password_reset_form: PasswordReset
		self.data: dict

		self.password_error: str = ""
		self.code_error: str = ""

	def get(self, request):
		self.password_reset_form = PasswordReset(request.GET)
		return self.redirect_reset(request=request)

	def post(self, request):
		self.password_reset_form = PasswordReset(request.POST)
		if self.password_reset_form.is_valid():
			self.data = self.password_reset_form.cleaned_data
			return self.verify_code(request=request)
		
		return self.redirect_reset(request=request)

	def verify_code(self, request):
		if self.data.get('code') == request.session.get('code'):
			return self.check_password(request=request)
		
		self.code_error = 'Invalid Code'
		return self.redirect_reset(request=request)

	def check_password(self, request):
		if len(self.data.get('password')) > 8:
			return self.both_matched(request=request)
		
		self.password_error = 'Password must be greater than 8 character'
		return self.redirect_reset(request=request)

	def both_matched(self, request):	
		conform_password = self.data.get('conform_password')
		if self.data.get('password') == conform_password:
			user = UserInfo.objects.filter(id=request.session.get('id')).first()
			if user:
				user.password = make_password(conform_password)
				user.save()
				sendemail(email_to=user.email, subject=self.subject, message=self.message)
				del request.session['code']
				self.delete_all_unexpired_sessions_for_user(request=request, user=user)
				self.password_error = 'your password has been reset successfully try to Signin'
				return self.redirect_reset(request=request)
			
			self.password_error = 'Try again later' 
			return self.redirect_reset(request=request)
		
		self.password_error = 'Password not matched'
		return self.redirect_reset(request=request)


	def redirect_reset(self, request):
		return render(request, 'forgotpassword.html', {
					'password_reset_form': self.password_reset_form,
					'password_error': self.password_error,
					'code_error': self.code_error,
				})
	
	def delete_all_unexpired_sessions_for_user(self, request, user):
		session_key = request.session.session_key
		user_sessions = UserSession.objects.filter(user=user).all()
		for user_session in user_sessions:
			user_session_key = user_session.session_key
			if  user_session_key != session_key:
				session = Session.objects.filter(session_key=user_session_key)
				if session.exists():
					session.delete()
				user_session.delete()



class LogoutView(View):
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(**kwargs)	

	def get(self, request):
		self.delete_sessions_for_user(request=request)
		return HttpResponseRedirect(reverse('login'))	
	
	def delete_sessions_for_user(self, request):
		session_key = request.session.session_key
		user_session = UserSession.objects.filter(session_key=session_key).first()
		if user_session:
			session = Session.objects.filter(session_key=session_key)
			if session.exists():
				session.delete()
			user_session.delete()
