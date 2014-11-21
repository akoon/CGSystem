# -*- coding: utf-8 -*-
'''
FormModel 前端Form类
'''
from django.db import models
from django.forms import ModelForm
from models import UserProfile, Position

class UserForm(ModelForm):
    class Meta:
        model = UserProfile
    
    
class PositionForm(ModelForm):
    class Meta:
        model = Position