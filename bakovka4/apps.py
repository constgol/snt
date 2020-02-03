from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class Bakovka4Config(AppConfig):
    name = 'bakovka4'


class Bakovka4AdminConfig(AdminConfig):
    default_site = 'bakovka4.admin.Bakovka4AdminSite'

