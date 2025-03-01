from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_contact_form_email, send_contact_response_email
from .models import ContactForm, ResponseTemplate, Banner, PracticeArea, Lawyer, BlogPost, ContactInfo, CaseStudy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import BannerForm, PracticeAreaForm, LawyerForm, BlogPostForm, ContactInfoForm, CaseStudyForm

def index(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    practices = PracticeArea.objects.all().order_by('order')
    cases = CaseStudy.objects.all().order_by('-created_at')
    blogs = BlogPost.objects.all().order_by('-created_at')
    context = {
        'title': 'Ana Sayfa - Hukuk Bürosu',
        'is_home': True,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
        'practices': practices,
        'cases': cases,
        'blogs': blogs,
    }
    return render(request, 'index.html', context)

def coming_soon(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Sayfa Bulunamadı',
        'is_home': False,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'coming-soon.html', context)

def about(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Hakkımızda',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'about.html', context)

def attorney(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Avukatlarımız',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'attorney.html', context)

def attorney_details(request, id):
    # Burada veritabanından avukat detayları çekilecek
    return render(request, 'attorney-details.html', {'title': 'Avukat Detayları'})

def practice(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Uzmanlık Alanlarımız',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'practice.html', context)

def practice_details(request, id):
    # Burada veritabanından uzmanlık alanı detayları çekilecek
    return render(request, 'practice-details.html', {'title': 'Uzmanlık Alanı Detayları'})

def case_study(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Örnek Davalar',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'case-study.html', context)

def case_study_details(request, id):
    # Burada veritabanından dava detayları çekilecek
    return render(request, 'case-study-details.html', {'title': 'Dava Detayları'})

def blog(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Blog',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'blog.html', context)

def blog_details(request, id):
    blog = get_object_or_404(BlogPost, id=id)
    recent_posts = BlogPost.objects.filter(is_active=True).exclude(id=id).order_by('-publish_date')[:3]
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'title': blog.title,
        'blog': blog,
        'recent_posts': recent_posts,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'blog-details.html', context)

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
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'İletişim',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'contact.html', context)

def appointment(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Randevu talebiniz alındı.'})
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Randevu',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'appointment.html', context)

def privacy_policy(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Gizlilik Politikası',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'privacy-policy.html', context)

def terms_conditions(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Kullanım Koşulları',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'terms-conditions.html', context)

@require_http_methods(["POST"])
def contact_form_submit(request):
    try:
        # Form verilerini al
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone_number'),  # HTML'deki name ile eşleştirdik
            'subject': request.POST.get('msg_subject'), # HTML'deki name ile eşleştirdik
            'message': request.POST.get('message')
        }
        
        # Zorunlu alanları kontrol et
        if not all(data.values()):
            return JsonResponse({
                'status': 'error',
                'message': 'Lütfen tüm alanları doldurunuz.'
            })
        
        # ContactForm modelini kullanarak kaydet
        contact = ContactForm.objects.create(**data)
        
        # Mail gönder
        try:
            send_contact_form_email(contact)
        except Exception as e:
            print(f"Mail gönderme hatası: {e}")
            # Mail gönderilemese bile form kaydedildi, kullanıcıya başarılı mesajı göster
        
        return JsonResponse({
            'status': 'success',
            'message': 'Mesajınız başarıyla alındı. En kısa sürede size dönüş yapacağız.'
        })
        
    except Exception as e:
        print(f"Form işleme hatası: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Mesajınız gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.'
        })

@login_required
def message_list(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    messages = ContactForm.objects.all().order_by('-created_at')
    paginator = Paginator(messages, 10)  # Her sayfada 10 mesaj
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    
    context = {
        'title': 'İletişim Formları',
        'messages': messages,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/messages/list.html', context)

@login_required
def message_response(request, form_id):
    contact_form = get_object_or_404(ContactForm, id=form_id)
    templates = ResponseTemplate.objects.filter(is_active=True)
    
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
            
            return redirect('webui:message_list')
    
    context = {
        'title': f'#{contact_form.id} Numaralı Mesajı Yanıtla',
        'contact_form': contact_form,
        'templates': templates,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/messages/response.html', context)

def get_template(request, template_id):
    template = get_object_or_404(ResponseTemplate, id=template_id)
    return JsonResponse({
        'content': template.content
    })

# Login view
def login_view(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Giriş',
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }   
    if request.user.is_authenticated:
        return redirect('webui:message_list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'webui:message_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return render(request, 'webui/auth/login.html', context)

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yapıldı.')
    return redirect('webui:login')

def get_unread_count(user):
    return ContactForm.objects.filter(is_read=False).count()

def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def management_dashboard(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Yönetim Paneli',
        'active_menu': 'dashboard',
        'banner_count': Banner.objects.count(),
        'practice_count': PracticeArea.objects.count(),
        'lawyer_count': Lawyer.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/dashboard.html', context)

@login_required
@user_passes_test(is_staff_user)
def banner_list(request):
    banners = Banner.objects.all().order_by('-created_at')
    paginator = Paginator(banners, 10)
    page = request.GET.get('page')
    banners = paginator.get_page(page)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Banner Yönetimi',
        'active_menu': 'banner',
        'banners': banners,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/banner_list.html', context)

@login_required
@user_passes_test(is_staff_user)
def banner_create(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner başarıyla oluşturuldu.')
            return redirect('webui:banner_list')
    else:
        form = BannerForm()
    
    context = {
        'title': 'Yeni Banner Ekle',
        'active_menu': 'banner',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/banner_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def banner_edit(request, id):
    banner = get_object_or_404(Banner, id=id)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner başarıyla güncellendi.')
            return redirect('webui:banner_list')
    else:
        form = BannerForm(instance=banner)
    
    context = {
        'title': 'Banner Düzenle',
        'active_menu': 'banner',
        'form': form,
        'banner': banner,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/banner_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def banner_delete(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    messages.success(request, 'Banner başarıyla silindi.')
    return redirect('webui:banner_list')

# Practice Area Views
@login_required
@user_passes_test(is_staff_user)
def practice_list(request):
    practices = PracticeArea.objects.all().order_by('order')
    paginator = Paginator(practices, 10)
    page = request.GET.get('page')
    practices = paginator.get_page(page)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Uzmanlık Alanları',
        'active_menu': 'practice',
        'practices': practices,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/practice_list.html', context)

@login_required
@user_passes_test(is_staff_user)
def practice_create(request):
    if request.method == 'POST':
        form = PracticeAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Uzmanlık alanı başarıyla oluşturuldu.')
            return redirect('webui:practice_list')
    else:
        form = PracticeAreaForm()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Yeni Uzmanlık Alanı Ekle',
        'active_menu': 'practice',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/practice_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def practice_edit(request, id):
    practice = get_object_or_404(PracticeArea, id=id)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = PracticeAreaForm(request.POST, instance=practice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Uzmanlık alanı başarıyla güncellendi.')
            return redirect('webui:practice_list')
    else:
        form = PracticeAreaForm(instance=practice)
    
    context = {
        'title': 'Uzmanlık Alanı Düzenle',
        'active_menu': 'practice',
        'form': form,
        'practice': practice,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/practice_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def practice_delete(request, id):
    practice = get_object_or_404(PracticeArea, id=id)
    practice.delete()
    messages.success(request, 'Uzmanlık alanı başarıyla silindi.')
    return redirect('webui:practice_list')

# Lawyer Views
@login_required
@user_passes_test(is_staff_user)
def lawyer_list(request):
    lawyers = Lawyer.objects.all().order_by('order')
    paginator = Paginator(lawyers, 10)
    page = request.GET.get('page')
    lawyers = paginator.get_page(page)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Avukatlar',
        'active_menu': 'lawyer',
        'lawyers': lawyers,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/lawyer_list.html', context)

@login_required
@user_passes_test(is_staff_user)
def lawyer_create(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avukat başarıyla eklendi.')
            return redirect('webui:lawyer_list')
    else:
        form = LawyerForm()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Yeni Avukat Ekle',
        'active_menu': 'lawyer',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/lawyer_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def lawyer_edit(request, id):
    lawyer = get_object_or_404(Lawyer, id=id)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES, instance=lawyer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avukat bilgileri başarıyla güncellendi.')
            return redirect('webui:lawyer_list')
    else:
        form = LawyerForm(instance=lawyer)
    
    context = {
        'title': 'Avukat Düzenle',
        'active_menu': 'lawyer',
        'form': form,
        'lawyer': lawyer,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/lawyer_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def lawyer_delete(request, id):
    lawyer = get_object_or_404(Lawyer, id=id)
    lawyer.delete()
    messages.success(request, 'Avukat başarıyla silindi.')
    return redirect('webui:lawyer_list')

# Blog Views
@login_required
@user_passes_test(is_staff_user)
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-publish_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Blog Yazıları',
        'active_menu': 'blog',
        'posts': posts,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/blog_list.html', context)

@login_required
@user_passes_test(is_staff_user)
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog yazısı başarıyla oluşturuldu.')
            return redirect('webui:blog_list')
    else:
        form = BlogPostForm()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Yeni Blog Yazısı',
        'active_menu': 'blog',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/blog_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def blog_edit(request, id):
    post = get_object_or_404(BlogPost, id=id)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog yazısı başarıyla güncellendi.')
            return redirect('webui:blog_list')
    else:
        form = BlogPostForm(instance=post)
    
    context = {
        'title': 'Blog Yazısı Düzenle',
        'active_menu': 'blog',
        'form': form,
        'post': post,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/blog_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def blog_delete(request, id):
    post = get_object_or_404(BlogPost, id=id)
    post.delete()
    messages.success(request, 'Blog yazısı başarıyla silindi.')
    return redirect('webui:blog_list')

# Contact Info Views
@login_required
@user_passes_test(is_staff_user)
def contact_info(request):
    info = ContactInfo.objects.first()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'İletişim Bilgileri',
        'active_menu': 'contact',
        'info': info,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/contact_info.html', context)

@login_required
@user_passes_test(is_staff_user)
def contact_info_edit(request):
    info = ContactInfo.objects.first()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'İletişim bilgileri başarıyla güncellendi.')
            return redirect('webui:contact_info')
    else:
        form = ContactInfoForm(instance=info)
    
    context = {
        'title': 'İletişim Bilgilerini Düzenle',
        'active_menu': 'contact',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/contact_info_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def case_list(request):
    cases = CaseStudy.objects.all().order_by('-is_featured', 'order', '-start_date')
    paginator = Paginator(cases, 10)
    page = request.GET.get('page')
    cases = paginator.get_page(page)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'title': 'Örnek Davalar',
        'active_menu': 'case',
        'cases': cases,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/case_list.html', context)

@login_required
@user_passes_test(is_staff_user)
def case_create(request):
    if request.method == 'POST':
        form = CaseStudyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dava başarıyla oluşturuldu.')
            return redirect('webui:case_list')
    else:
        form = CaseStudyForm()
    
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'title': 'Yeni Dava Ekle',
        'active_menu': 'case',
        'form': form,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/case_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def case_edit(request, id):
    case = get_object_or_404(CaseStudy, id=id)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        form = CaseStudyForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dava başarıyla güncellendi.')
            return redirect('webui:case_list')
    else:
        form = CaseStudyForm(instance=case)
    
    context = {
        'title': 'Dava Düzenle',
        'active_menu': 'case',
        'form': form,
        'case': case,
        'unread_count': get_unread_count(request.user) if request.user.is_authenticated else 0,
        'contact_info': contact_info,
    }
    return render(request, 'webui/management/case_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def case_delete(request, id):
    case = get_object_or_404(CaseStudy, id=id)
    case.delete()
    messages.success(request, 'Dava başarıyla silindi.')
    return redirect('webui:case_list')

