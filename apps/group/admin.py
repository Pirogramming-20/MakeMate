from django.contrib import admin

from .models import Group, MemberState, AdminState, Idea

# Register your models here.
admin.site.register(Group)
admin.site.register(MemberState)
admin.site.register(AdminState)
admin.site.register(Idea)
