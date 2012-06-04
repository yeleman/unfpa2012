#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from unfpa_web import views
from bolibana.web import views as bviews
from bolibana.web.decorators import provider_permission
from settings import STATIC_ROOT, MEDIA_ROOT

urlpatterns = patterns('',
    url(r'^/?$', views.dashboard.dashboard, name='index'),
    url(r'^profile/$', bviews.profile.edit_profile, name='profile'),

    # login
    url(r'^login/$', 'django.contrib.auth.views.login', \
         {'template_name': 'login_django.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', \
         {'template_name': 'logout_django.html'}, name='logout'),

    # reports
    url(r'^reports/(?P<report_type>maternal|children|commodities)/'
         '(?P<period_type>weekly|monthly|quarterly|annual)/'
         '(?P<period_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}|[0-9]{1,2}\-[0-9]{4})/?$',
        views.reports.report_chooser, name='reports'),

    # CREDOS
    url(r'^credos/pregnancy/$', views.pregnancy.pregnancy, name='pregnancy'),
    url(r'^credos/birth/$', views.birth.birth, name='birth'),
    url(r'^credos/death/$', views.death.death, name='death'),

    # ANTIM : USERS
    url(r'^users/?$', \
        provider_permission('can_manage_users')(bviews.providers. \
                                                ProvidersListView.as_view()), \
        name='list_users'),
    url(r'^users/add$', bviews.providers.add_edit_user, name='add_user'),
    url(r'^users/edit/(?P<user_id>[0-9]+)$', \
        bviews.providers.add_edit_user, name='edit_user'),
    url(r'^users/disable/(?P<user_id>[0-9]+)$', \
        bviews.providers.enable_disable_user, name='disable_user', \
        kwargs={'activate': False}),
    url(r'^users/enable/(?P<user_id>[0-9]+)$', \
        bviews.providers.enable_disable_user, name='enable_user', \
        kwargs={'activate': True}),
    url(r'^users/new_password/(?P<user_id>[0-9]+)$', \
        bviews.providers.password_user, name='password_user'),

    # ANTIM : ENTITIES
    url(r'^entities/?$', \
        provider_permission('can_manage_entities')(bviews.entities. \
                                                EntitiesListView.as_view()), \
        name='list_entities'),
    url(r'^entities/add$', bviews.entities.add_edit_entity, name='add_entity'),
    url(r'^entities/edit/(?P<entity_id>[0-9]+)$', \
        bviews.entities.add_edit_entity, name='edit_entity'),

    # static web pages
     url(r'^support/$', views.dashboard.contact, name='support'),
     url(r'^help/$', direct_to_template, \
         {'template': 'help.html'}, name='help'),
     url(r'^about/$', direct_to_template, \
         {'template': 'about.html'}, name='about'),

     url(r'^annuaire/$', bviews.addressbook.addressbook, name='addressbook'),

    # development only
    url(r'^static/admin/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': os.path.join(os.path.dirname(\
                                            os.path.abspath(admin.__file__)), \
                               'media'), 'show_indexes': True}, \
             name='static_admin'),

    url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': STATIC_ROOT, 'show_indexes': True}, \
             name='static'),

    url(r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': MEDIA_ROOT, 'show_indexes': True}, \
             name='media'),

)
