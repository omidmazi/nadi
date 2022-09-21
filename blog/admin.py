from django.contrib import admin
from .models import Post,Author,PostAdmin,Tag,Comment,CommentAdmin,Product,Order,OrderAdmin



admin.site.register(Post,PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)