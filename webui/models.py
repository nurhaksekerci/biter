from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
import re
from django.utils import timezone

def tr_slugify(text):
    """
    Türkçe karakterleri İngilizce karakterlere dönüştürüp slug oluşturur
    """
    tr_chars = {
        'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U',
        'ş': 's', 'Ş': 'S',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ç': 'c', 'Ç': 'C',
    }
    
    for char in tr_chars:
        text = text.replace(char, tr_chars[char])
    
    # Özel karakterleri kaldır ve küçük harfe çevir
    text = text.lower()
    # Birden fazla boşlukları tek boşluğa çevir
    text = re.sub(r'\s+', ' ', text)
    # slugify uygula
    return slugify(text)

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = RichTextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='banner/', verbose_name="Banner Görseli")
    button_text = models.CharField(max_length=50, verbose_name="Buton Metni")
    button_url = models.CharField(max_length=100, verbose_name="Buton URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PracticeArea(models.Model):
    icon = models.CharField(max_length=50, verbose_name="Flaticon İkonu", help_text="Örn: flaticon-law")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    button_text = models.CharField(max_length=50, verbose_name="Buton Metni", default="Devamını Oku")
    button_url = models.CharField(max_length=100, verbose_name="Buton URL")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "Uzmanlık Alanı"
        verbose_name_plural = "Uzmanlık Alanları"
        ordering = ['order']

    def __str__(self):
        return self.title

class Expertise(models.Model):
    icon = models.CharField(max_length=50, verbose_name="Flaticon İkonu")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    animation_delay = models.CharField(max_length=10, verbose_name="Animasyon Gecikmesi", default=".3s")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "Uzmanlık"
        verbose_name_plural = "Uzmanlıklar"
        ordering = ['order']

    def __str__(self):
        return self.title

class Portfolio(models.Model):
    image = models.ImageField(upload_to='portfolio/', verbose_name="Görsel")
    category = models.CharField(max_length=50, verbose_name="Kategori")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    date = models.DateField(verbose_name="Tarih")
    url = models.CharField(max_length=100, verbose_name="URL")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "Portföy"
        verbose_name_plural = "Portföy"
        ordering = ['order']

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    image = models.ImageField(upload_to='blog/', verbose_name="Görsel")
    category = models.CharField(max_length=50, verbose_name="Kategori")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    content = RichTextField(verbose_name="İçerik")
    author = models.CharField(max_length=100, verbose_name="Yazar")
    publish_date = models.DateField(verbose_name="Yayın Tarihi")
    slug = models.SlugField(unique=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = tr_slugify(self.title)
        super().save(*args, **kwargs)

class ContactInfo(models.Model):
    address = models.TextField(verbose_name="Adres")
    email1 = models.EmailField(verbose_name="E-posta 1")
    email2 = models.EmailField(verbose_name="E-posta 2", blank=True)
    phone1 = models.CharField(max_length=20, verbose_name="Telefon 1")
    phone2 = models.CharField(max_length=20, verbose_name="Telefon 2", blank=True)
    map_url = models.URLField(verbose_name="Harita URL")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "İletişim Bilgisi"
        verbose_name_plural = "İletişim Bilgileri"

    def __str__(self):
        return self.address

class ContactForm(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    subject = models.CharField(max_length=200, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(verbose_name="Yanıt", blank=True, null=True)
    response_date = models.DateTimeField(verbose_name="Yanıt Tarihi", blank=True, null=True)
    is_read = models.BooleanField(default=False, verbose_name="Okundu")

    class Meta:
        verbose_name = "İletişim Formu"
        verbose_name_plural = "İletişim Formları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def save(self, *args, **kwargs):
        if self.response and not self.response_date:
            self.response_date = timezone.now()
        super().save(*args, **kwargs)

class Lawyer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad")
    surname = models.CharField(max_length=100, verbose_name="Soyad")
    title = models.CharField(max_length=100, verbose_name="Ünvan", help_text="Örn: Avukat, Stajyer Avukat")
    image = models.ImageField(upload_to='lawyers/', verbose_name="Fotoğraf")
    description = RichTextField(verbose_name="Hakkında")
    education = RichTextField(verbose_name="Eğitim Bilgileri")
    experience = models.PositiveIntegerField(verbose_name="Deneyim (Yıl)")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn", blank=True)
    twitter = models.URLField(verbose_name="Twitter", blank=True)
    facebook = models.URLField(verbose_name="Facebook", blank=True)
    instagram = models.URLField(verbose_name="Instagram", blank=True)
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, verbose_name="URL")

    class Meta:
        verbose_name = "Avukat"
        verbose_name_plural = "Avukatlar"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.title} {self.name} {self.surname}"

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def get_absolute_url(self):
        return reverse('webui:lawyer_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = tr_slugify(f"{self.name} {self.surname}")
        super().save(*args, **kwargs)

class LawyerExpertise(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='expertise_areas', verbose_name="Avukat")
    practice_area = models.ForeignKey(PracticeArea, on_delete=models.CASCADE, verbose_name="Uzmanlık Alanı")
    experience_years = models.PositiveIntegerField(verbose_name="Bu Alandaki Deneyim (Yıl)")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    is_primary = models.BooleanField(default=False, verbose_name="Ana Uzmanlık Alanı Mı?")
    order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        verbose_name = "Avukat Uzmanlık Alanı"
        verbose_name_plural = "Avukat Uzmanlık Alanları"
        ordering = ['order']
        unique_together = ['lawyer', 'practice_area']  # Bir avukatın aynı uzmanlık alanı tekrar eklenemesin

    def __str__(self):
        return f"{self.lawyer.get_full_name()} - {self.practice_area.title}"

class LawyerCertificate(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='certificates', verbose_name="Avukat")
    title = models.CharField(max_length=200, verbose_name="Sertifika Adı")
    institution = models.CharField(max_length=200, verbose_name="Veren Kurum")
    date = models.DateField(verbose_name="Alınma Tarihi")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    image = models.ImageField(upload_to='certificates/', verbose_name="Sertifika Görseli", blank=True)
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    class Meta:
        verbose_name = "Sertifika"
        verbose_name_plural = "Sertifikalar"
        ordering = ['order', '-date']

    def __str__(self):
        return f"{self.lawyer.get_full_name()} - {self.title}"

class ResponseTemplate(models.Model):
    title = models.CharField(max_length=100, verbose_name="Şablon Başlığı")
    content = models.TextField(verbose_name="Şablon İçeriği")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        verbose_name = "Yanıt Şablonu"
        verbose_name_plural = "Yanıt Şablonları"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class CaseStudy(models.Model):
    CASE_STATUS_CHOICES = (
        ('ongoing', 'Devam Ediyor'),
        ('won', 'Kazanıldı'),
        ('lost', 'Kaybedildi'),
        ('settled', 'Uzlaşma Sağlandı'),
        ('appealed', 'Temyizde'),
    )

    CASE_TYPE_CHOICES = (
        ('Ceza Hukuku', 'Ceza Hukuku'),
        ('Medeni Hukuk', 'Medeni Hukuk'),
        ('Ticaret Hukuku', 'Ticaret Hukuku'),
        ('İş Hukuku', 'İş Hukuku'),
        ('Aile Hukuku', 'Aile Hukuku'),
        ('Siber Hukuk', 'Siber Hukuk'),
        ('Eğitim Hukuku', 'Eğitim Hukuku'),
        ('Miras Hukuku', 'Miras Hukuku'),
        ('İcra Hukuku', 'İcra Hukuku'),
        ('İdare Hukuku', 'İdare Hukuku'),
        ('Vergi Hukuku', 'Vergi Hukuku'),
        ('Diğer', 'Diğer'),
    )

    title = models.CharField(max_length=200, verbose_name="Dava Başlığı")
    slug = models.SlugField(unique=True, verbose_name="URL")
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, verbose_name="Dava Türü")
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, verbose_name="Durum")
    
    summary = models.TextField(verbose_name="Özet")
    content = RichTextField(verbose_name="Detaylı Açıklama")
    
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    
    client_type = models.CharField(max_length=100, verbose_name="Müvekkil Türü", help_text="Örn: Bireysel, Kurumsal")
        
    result = models.TextField(verbose_name="Sonuç", blank=True)
    
    featured_image = models.ImageField(upload_to='cases/', verbose_name="Kapak Görseli", blank=True)
    
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan Dava")
    is_public = models.BooleanField(default=True, verbose_name="Yayında")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    meta_title = models.CharField(max_length=200, verbose_name="Meta Başlık", blank=True)
    meta_description = models.TextField(verbose_name="Meta Açıklama", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Örnek Dava"
        verbose_name_plural = "Örnek Davalar"
        ordering = ['-is_featured', 'order', '-start_date']

    def __str__(self):
        return f"{self.title} ({self.get_case_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = tr_slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.summary[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('webui:case_detail', kwargs={'slug': self.slug})

    @property
    def duration(self):
        """Dava süresini hesaplar"""
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (timezone.now().date() - self.start_date).days

    @property
    def is_active(self):
        """Davanın aktif olup olmadığını kontrol eder"""
        return self.status == 'ongoing'
