#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou


from django.shortcuts import render

def birth(request):
	context = {'category': 'birth', 'eg': 'birth'}
	return render(request, 'birth.html', context)