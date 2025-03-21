from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, ContactMessage, ApprovedRestaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cuisine_type',
        'price_range',
        'display_rating',
        'city',
        'approved',
        'display_contact',
        'submitted_by',
    )
    
    list_filter = (
        'approved',
        'cuisine_type',
        'price_range',
        'delivery_available',
        'takeout_available',
        'city',
    )
    
    search_fields = (
        'name',
        'description',
        'street_address',
        'city',
        'state',
        'country',
        'submitted_by__username',
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
        'submitted_by',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'description',
                'cuisine_type',
                'price_range',
                'average_rating',
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'email',
                'website',
            )
        }),
        ('Business Details', {
            'fields': (
                ('opentime', 'closetime'),
                ('delivery_available', 'takeout_available'),
            )
        }),
        ('Location', {
            'fields': (
                'street_address',
                ('city', 'state'),
                ('postal_code', 'country'),
                ('latitude', 'longitude'),
            )
        }),
        ('Meta Information', {
            'fields': (
                'approved',
                'submitted_by',
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['approve_restaurants']
    
    def display_rating(self, obj):
        """Display rating with stars"""
        stars = '★' * int(round(obj.average_rating))
        # Convert the float to string with 1 decimal place before passing to format_html
        rating = '{:.1f}'.format(obj.average_rating)
        return format_html('<span style="color: #FFD700;">{}</span> ({})', stars, rating)
    display_rating.short_description = 'Rating'
    
    def display_contact(self, obj):
        """Display contact information"""
        contacts = []
        if obj.phone:
            contacts.append(f'📞 {obj.phone}')
        if obj.email:
            contacts.append(f'✉ {obj.email}')
        return ' | '.join(contacts) if contacts else '-'
    display_contact.short_description = 'Contact'
    
    def approve_restaurants(self, request, queryset):
        """Approve selected restaurants and move them to ApprovedRestaurant."""
        approved_count = 0
        for restaurant in queryset:
            if not restaurant.approved:
                restaurant.approve()
                approved_count += 1
        self.message_user(request, f'{approved_count} restaurant(s) were successfully approved and moved to Approved Restaurants.')
    approve_restaurants.short_description = 'Approve selected restaurants'
    
    
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

admin.site.register(ContactMessage, ContactMessageAdmin)

# Register ApprovedRestaurant in the admin panel
@admin.register(ApprovedRestaurant)
class ApprovedRestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cuisine_type',
        'price_range',
        'average_rating',
        'city',
        'submitted_by',
    )
    search_fields = (
        'name',
        'description',
        'street_address',
        'city',
        'state',
        'country',
        'submitted_by__username',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'submitted_by',
    )

