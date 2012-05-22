#!/usr/bin/env python
# encoding=utf-8
# maintainer: 


from django.shortcuts import render

def death(request):
	context = {'category': 'death', 'eg': 'death'}
	return render(request, 'death.html', context)