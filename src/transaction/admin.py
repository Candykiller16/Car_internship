from django.contrib import admin
from src.transaction.models import FromDealerToShowroomTransaction, FromShowroomToCustomerTransaction


@admin.register(FromDealerToShowroomTransaction)
class FromDealerToShowroomTransactionsAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
    list_filter = ("discount", "created")


@admin.register(FromShowroomToCustomerTransaction)
class FormShowroomToCustomerTransactionsAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
    list_filter = ("discount", "created")
