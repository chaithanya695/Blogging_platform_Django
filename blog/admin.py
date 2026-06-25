from django.contrib import admin
from .models import Post,Category,Comment

# Register your models here.
class post_admin(admin.ModelAdmin):
    list_display=['title','content','author','created_at','updated_at']
admin.site.register(Post,post_admin)

admin.site.register(Category)
admin.site.register(Comment)
