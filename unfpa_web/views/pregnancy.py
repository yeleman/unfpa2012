#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad


from django.shortcuts import render

def pregnancy(request):
	context = {'category': 'pregnancy', 'eg': 'pregnancy'}
	return render(request, 'pregnancy.html', context)