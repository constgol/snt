from django.contrib import admin


class Bakovka4AdminSite(admin.AdminSite):
    site_header = 'Баковка 4'


Bakovka4AdminSite(name='bakovka4adm')

