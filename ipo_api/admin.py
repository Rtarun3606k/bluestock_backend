from django.contrib import admin
from .models import Company, IPO, UserProfile

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ('company', 'price_band', 'open_date', 'close_date', 'issue_size', 'status')
    list_filter = ('status', 'open_date', 'close_date', 'listing_date')
    search_fields = ('company__name', 'issue_type')
    date_hierarchy = 'open_date'
    ordering = ('-open_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('IPO Details', {
            'fields': (
                ('price_band_min', 'price_band_max'),
                ('open_date', 'close_date', 'listing_date'),
                'issue_size', 'issue_type', 'status'
            )
        }),
        ('After Listing', {
            'fields': ('ipo_price', 'listing_price', 'current_market_price'),
            'classes': ('collapse',),
            'description': 'Information available after IPO listing'
        }),
        ('Documents', {
            'fields': ('rhp_document', 'drhp_document'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_client', 'api_key')
    list_filter = ('is_client',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('api_key',)
