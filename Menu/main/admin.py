from django.contrib import admin
from .models import Special, Foods, Category
from unfold.admin import ModelAdmin as UnfoldModelAdmin

# Option 1: Using the decorator for each model
@admin.register(Special)
class SpecialAdmin(UnfoldModelAdmin):
    pass

@admin.register(Foods)
class FoodsAdmin(UnfoldModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(UnfoldModelAdmin):
    pass

# Option 2: Using admin.site.register() - equivalent to the decorator approach
# admin.site.register(Special, UnfoldModelAdmin)
# admin.site.register(Foods, UnfoldModelAdmin)
# admin.site.register(Category, UnfoldModelAdmin)