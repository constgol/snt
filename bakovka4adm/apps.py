from django.contrib.admin.apps import AdminConfig


class Bakovka4AdminConfig(AdminConfig):
    default_site = 'bakovka4adm.admin.Bakovka4AdminSite'

