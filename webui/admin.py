from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    ContactForm, ResponseTemplate, Banner, PracticeArea, Lawyer, BlogPost, ContactInfo,
    Expertise, Portfolio, LawyerExpertise, LawyerCertificate, CaseStudy
)

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read', 'response_status', 'actions_buttons')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def response_status(self, obj):
        if obj.response:
            return format_html('<span style="color: green;">✓ Yanıtlandı</span>')
        return format_html('<span style="color: red;">✗ Yanıtlanmadı</span>')
    response_status.short_description = 'Yanıt Durumu'

    def actions_buttons(self, obj):
        if not obj.response:
            url = reverse('admin:webui_contactform_response', args=[obj.id])
            return format_html(
                '<a class="button" href="{}">Yanıtla</a>',
                url
            )
        url = reverse('admin:webui_contactform_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Detay</a>',
            url
        )
    actions_buttons.short_description = 'İşlemler'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:form_id>/response/',
                self.admin_site.admin_view(self.response_view),
                name='webui_contactform_response',
            ),
        ]
        return custom_urls + urls

    def response_view(self, request, form_id):
        from django.shortcuts import get_object_or_404, redirect
        from django.template.response import TemplateResponse
        from django.contrib import messages
        from .utils import send_contact_response_email

        contact_form = get_object_or_404(ContactForm, id=form_id)
        
        if request.method == 'POST':
            response_text = request.POST.get('response')
            if response_text:
                contact_form.response = response_text
                contact_form.is_read = True
                contact_form.save()
                
                try:
                    send_contact_response_email(contact_form, response_text)
                    messages.success(request, 'Yanıt başarıyla gönderildi.')
                except Exception as e:
                    messages.error(request, f'Yanıt gönderilirken bir hata oluştu: {str(e)}')
                
                return redirect('admin:webui_contactform_changelist')
        
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'contact_form': contact_form,
            'title': f'#{contact_form.id} Numaralı İletişim Formunu Yanıtla',
        }
        
        return TemplateResponse(request, 'admin/webui/contactform/response.html', context)

@admin.register(ResponseTemplate)
class ResponseTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    ordering = ('order', 'title')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('-id',)

@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'title', 'experience', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'surname', 'title', 'description', 'education')
    ordering = ('order',)

    def get_full_name(self, obj):
        return f"{obj.name} {obj.surname}"
    get_full_name.short_description = 'Ad Soyad'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish_date', 'is_active')
    list_filter = ('is_active', 'category', 'publish_date')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email1', 'phone1', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('address', 'email1', 'email2', 'phone1', 'phone2')

@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'animation_delay', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'category')
    ordering = ('order',)

@admin.register(LawyerExpertise)
class LawyerExpertiseAdmin(admin.ModelAdmin):
    list_display = ('lawyer', 'practice_area', 'experience_years', 'is_primary', 'order')
    list_filter = ('is_primary', 'practice_area')
    search_fields = ('lawyer__name', 'lawyer__surname', 'practice_area__title')
    ordering = ('order',)

@admin.register(LawyerCertificate)
class LawyerCertificateAdmin(admin.ModelAdmin):
    list_display = ('lawyer', 'title', 'institution', 'date', 'order', 'is_active')
    list_filter = ('is_active', 'institution', 'date')
    search_fields = ('title', 'institution', 'lawyer__name', 'lawyer__surname')
    ordering = ('order', '-date')

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'case_type', 'status', 'start_date', 'is_featured', 'is_public')
    list_filter = ('status', 'case_type', 'is_featured', 'is_public')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    ordering = ('-is_featured', 'order', '-start_date')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'case_type', 'status', 'client_type')
        }),
        ('İçerik', {
            'fields': ('summary', 'content', 'result')
        }),
        ('Tarihler', {
            'fields': ('start_date', 'end_date')
        }),
        ('Medya', {
            'fields': ('featured_image',)
        }),
        ('Görünürlük ve Sıralama', {
            'fields': ('is_featured', 'is_public', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )

    def get_duration(self, obj):
        return f"{obj.duration} gün"
    get_duration.short_description = 'Süre'

    def get_status_display(self, obj):
        status_colors = {
            'ongoing': 'blue',
            'won': 'green',
            'lost': 'red',
            'settled': 'orange',
            'appealed': 'purple'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_display.short_description = 'Durum'
