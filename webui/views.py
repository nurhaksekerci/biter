from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    context = {
        'title': 'Ana Sayfa - Hukuk Bürosu',
        'is_home': True
    }
    return render(request, 'index.html', context)

def not_found(request):
    context = {
        'title': 'Sayfa Bulunamadı',
        'is_home': False
    }
    return render(request, '404.html', context)

def about(request):
    return render(request, 'about.html', {'title': 'Hakkımızda'})

def attorney(request):
    return render(request, 'attorney.html', {'title': 'Avukatlarımız'})

def attorney_details(request, id):
    # Burada veritabanından avukat detayları çekilecek
    return render(request, 'attorney-details.html', {'title': 'Avukat Detayları'})

def practice(request):
    return render(request, 'practice.html', {'title': 'Uzmanlık Alanlarımız'})

def practice_details(request, id):
    # Burada veritabanından uzmanlık alanı detayları çekilecek
    return render(request, 'practice-details.html', {'title': 'Uzmanlık Alanı Detayları'})

def case_study(request):
    return render(request, 'case-study.html', {'title': 'Örnek Davalar'})

def case_study_details(request, id):
    # Burada veritabanından dava detayları çekilecek
    return render(request, 'case-study-details.html', {'title': 'Dava Detayları'})

def blog(request):
    return render(request, 'blog.html', {'title': 'Blog'})

def blog_details(request, id):
    # Burada veritabanından blog detayları çekilecek
    return render(request, 'blog-details.html', {'title': 'Blog Detayları'})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        subject = request.POST.get('msg_subject')
        message = request.POST.get('message')
        
        email_message = f"""
        İsim: {name}
        E-posta: {email}
        Telefon: {phone}
        Konu: {subject}
        Mesaj: {message}
        """
        
        try:
            send_mail(
                subject=f'İletişim Formu: {subject}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Mesajınız başarıyla gönderildi.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Mesaj gönderilirken bir hata oluştu.'})
    
    return render(request, 'contact.html')

def appointment(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Randevu talebiniz alındı.'})
    return render(request, 'appointment.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_conditions(request):
    return render(request, 'terms-conditions.html')

