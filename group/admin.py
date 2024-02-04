from django.contrib import admin
from .models import Group, MemberState, AdminState

# Register your models here.
admin.site.register(Group)
admin.site.register(MemberState)
admin.site.register(AdminState)
