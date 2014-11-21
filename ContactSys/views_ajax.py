# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from BaseSys.models import *

def people_detail(request):
    info = {}
    if request.method == 'GET':
        peoples = User.objects.filter(is_active = 1)
        i = 0
        l = []
        for p in peoples:
            try:
                profile = UserProfile.objects.get(user = p)
            except:
                profile = ''
            i +=1
            k = {}
            k['id'] = p.id
            k['user'] = p.username
            k['name'] = p.first_name           
            k['email'] = p.email
            if profile:
                k['sex'] = profile.sex
                k['phone'] = profile.phone
                if profile.department:
                    k['department'] = profile.department.name
                if profile.position:
                    k['position'] = profile.position.name
                if profile.thum:
                    k['img'] = profile.thum.url
                if profile.seatnumber:
                    k['seatnumber'] = profile.seatnumber
            k['is_superuser'] = p.is_superuser
            l.append(k)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))
