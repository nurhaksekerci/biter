from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from pathlib import Path

def send_contact_form_email(contact_form):
    """
    İletişim formu gönderildiğinde bildirim maili gönderir
    """
    subject = f'Yeni İletişim Formu Mesajı: {contact_form.subject}'
    
    # HTML içeriği oluştur
    html_content = render_to_string('emails/contact_form_notification.html', {
        'name': contact_form.name,
        'email': contact_form.email,
        'phone': contact_form.phone,
        'subject': contact_form.subject,
        'message': contact_form.message,
        'created_at': contact_form.created_at
    })
    
    # Text içeriği oluştur
    text_content = strip_tags(html_content)
    
    # Mail oluştur
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [settings.CONTACT_FORM_EMAIL]  # Alıcı e-posta adresi
    )
    
    # HTML içeriği ekle
    email.attach_alternative(html_content, "text/html")
    
    # Gönder
    email.send()

def send_contact_response_email(contact_form, response_text):
    """
    İletişim formuna verilen cevabı müvekkile gönderir
    """
    subject = f'Re: {contact_form.subject} - Biter Hukuk Bürosu Yanıtı'
    
    # Logo URL'sini oluştur
    if settings.DEBUG:
        # Geliştirme ortamında
        logo_url = 'https://biterhukuk.com.tr/static/assets/img/logo.png'
    else:
        # Prodüksiyon ortamında
        logo_url = settings.LOGO_URL
    
    # HTML içeriği oluştur
    html_content = render_to_string('emails/contact_form_response.html', {
        'name': contact_form.name,
        'subject': contact_form.subject,
        'message': contact_form.message,
        'created_at': contact_form.created_at,
        'response': response_text,
        'response_date': timezone.now(),
        'logo_url': logo_url,
        'office_address': settings.OFFICE_ADDRESS
    })
    
    # Mail oluştur
    email = EmailMultiAlternatives(
        subject,
        strip_tags(html_content),
        settings.DEFAULT_FROM_EMAIL,
        [contact_form.email]
    )
    
    # Logo dosyasını ekle
    try:
        logo_path = Path(settings.STATIC_ROOT) / 'assets/img/logo.png'
        if logo_path.exists():
            email.attach_file(str(logo_path))
    except Exception as e:
        # Logo eklenemezse devam et
        print(f"Logo eklenirken hata: {e}")
    
    # HTML içeriği ekle
    email.attach_alternative(html_content, "text/html")
    
    # Gönder
    email.send() 