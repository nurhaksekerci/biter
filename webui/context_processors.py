from .models import ContactForm

def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = ContactForm.objects.filter(is_read=False).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count} 