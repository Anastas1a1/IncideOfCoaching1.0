from django.contrib import admin
from .models import AdminProfile, File, UserProfile, Subscription, FileGoogle, FileTg


admin.site.register(AdminProfile)
admin.site.register(UserProfile)
admin.site.register(Subscription)
admin.site.register(File)
admin.site.register(FileGoogle)
admin.site.register(FileTg)

