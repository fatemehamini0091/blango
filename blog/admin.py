from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile

"""
 lets you create, edit and delete any Django model instances that you choose. 
"""
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)


class PostAdmin(admin.ModelAdmin):

  """
  When used in this way, some JavaScript is inserted 
  into the admin page so that the slug field updates when the title field changes. 
  """
  prepopulated_fields = {"slug": ("title",)}
  list_display = ('published_at', 'slug')
  # "exclude, fields, list_display"


admin.site.register(Post, PostAdmin)