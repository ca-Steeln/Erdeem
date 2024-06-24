
from django.contrib import admin

from .models import Member

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    model = Member
    exclude = ['password', 'groups', 'user_permissions', 'first_name', 'last_name']
    readonly_fields = ['username', 'email', 'is_superuser', 'is_staff', 'date_joined', 'last_login']

admin.site.register(Member, MemberAdmin)