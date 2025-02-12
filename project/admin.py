from django.contrib import admin
from django.utils.html import format_html
from .models import EverydayTask

@admin.register(EverydayTask)
class EverydayTaskAdmin(admin.ModelAdmin):
    list_display = ('day', 'status_colored')  
    list_filter = ['status'] 
    search_fields = ('day', 'quote_1', 'quote_2')  
    ordering = ('day',)
    def status_colored(self, obj):
        colors = {
            'Sports': 'red',
            'Mental growth and recovery': 'green',
            'Relaxation': 'blue',
            'Professional skill-building': 'orange',
            'Theoretical study': 'gray',
            'adaptation': 'yellow',
        }

        color = colors.get(obj.status, 'black')
        
        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<div style="width: 12px; height: 12px; border-radius: 50%; background-color: {}; margin-right: 10px;"></div>'
            '<span>{}</span>'
            '</div>', 
            color, obj.get_status_display()
        )

    status_colored.admin_order_field = 'status'
    status_colored.short_description = "Status"

