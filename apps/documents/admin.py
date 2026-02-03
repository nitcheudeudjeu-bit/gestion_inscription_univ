from django.contrib import admin
from django.utils.timezone import now
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "is_validated",
        "is_refused",
        "validated_at",
        "created_at",
    )

    list_filter = ("is_validated", "is_refused")
    search_fields = ("student__matricule", "student__email")

    actions = ["validate_documents", "refuse_documents"]

    @admin.action(description="✅ Valider les documents")
    def validate_documents(self, request, queryset):
        queryset.update(
            is_validated=True,
            is_refused=False,
            admin_comment="",
            validated_at=now()
        )

    @admin.action(description="❌ Refuser les documents")
    def refuse_documents(self, request, queryset):
        queryset.update(
            is_validated=False,
            is_refused=True,
            validated_at=None
        )

