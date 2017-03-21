from django.contrib import admin
from .models import Repairer, RepairerRating, Shop, Expertise, Customer, CustomerRating, Favourites, AUser

# Register your models here.

admin.site.register(Repairer)
admin.site.register(RepairerRating)
admin.site.register(Shop)
admin.site.register(Expertise)
admin.site.register(CustomerRating)
admin.site.register(Favourites)
admin.site.register(Customer)
admin.site.register(AUser)
#class CustomerRating(admin.ModelAdmin):
 #   list_display = Customer.
#class Favourites(admin.ModelAdmin):
 #   list_display = ('__all__')
#class Customer(admin.ModelAdmin):
 #   list_display = ('__all__')
#class AUser(admin.ModelAdmin):
 #   list_display = ('__all__')
#class Repairer(admin.ModelAdmin):
 #   list_display = ('__all__')
#class RepairerRating(admin.ModelAdmin):
 #   list_display = ('__all__')

#class Shop(admin.ModelAdmin):
 #   list_display = ('__all__')


#class Expertise(admin.ModelAdmin):
 #   list_display = ('__all__')