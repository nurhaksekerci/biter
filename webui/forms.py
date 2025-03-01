from django import forms
from django.forms import ModelForm
from .models import Banner, PracticeArea, Lawyer, BlogPost, ContactInfo, CaseStudy
from ckeditor.widgets import CKEditorWidget

class BannerForm(ModelForm):
    description = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='Açıklama'
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Önerilen görsel boyutu: 1920x814 piksel',
        label='Banner Görseli'
    )
    
    class Meta:
        model = Banner
        fields = ['title', 'description', 'image', 'button_text', 'button_url', 'is_active']
        labels = {
            'title': 'Başlık',
            'button_text': 'Buton Metni',
            'button_url': 'Buton URL',
            'is_active': 'Aktif'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PracticeAreaForm(ModelForm):
    ICON_CHOICES = (
        ('Temel İkonlar', (
            ('flaticon-balance', 'Terazi (Adalet)'),      # Adalet sembolü
            ('flaticon-lawyer', 'Hakim'),                 # Hakim figürü
            ('flaticon-law', 'Adliye'),                   # Adliye binası
            ('flaticon-judge', 'Mahkeme'),                # Mahkeme salonu
            ('flaticon-team', 'Avukatlar'),              # Avukat ekibi
        )),
        ('Hukuk Alanları', (
            ('flaticon-family', 'Aile Hukuku'),          # Aile figürü
            ('flaticon-inheritance', 'Miras Hukuku'),     # Miras sembolü
            ('flaticon-mortarboard', 'Eğitim Hukuku'),    # Mezuniyet
            ('flaticon-auction', 'İcra Hukuku'),          # Açık artırma
            ('flaticon-vulnerability', 'Siber Hukuk'),    # Güvenlik
            ('flaticon-money-bag', 'Ticaret Hukuku'),    # Para çantası
            ('flaticon-leader', 'İş Hukuku'),            # İş adamı
            ('flaticon-conversation', 'Arabuluculuk'),    # Konuşma
            ('flaticon-checkmark', 'Sözleşmeler'),       # Onay işareti
        )),
        ('Özel Hizmetler', (
            ('flaticon-experience', 'Tecrübe'),          # Deneyim
            ('flaticon-time', 'Acil Davalar'),           # Saat
            ('flaticon-download', 'Dosya Takibi'),       # İndirme
            ('flaticon-medal', 'Uzman Görüşü'),          # Madalya
            ('flaticon-support', 'Müvekkil İlişkileri'), # Destek
        )),
        ('Kurumsal', (
            ('flaticon-pin', 'Ofis Lokasyonu'),          # Konum
            ('flaticon-email', 'İletişim'),              # E-posta
            ('flaticon-call', 'Danışma'),                # Telefon
        ))
    )

    icon = forms.ChoiceField(
        choices=ICON_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'icon-select'
        }),
        label='İkon'
    )

    description = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='Açıklama'
    )
    
    class Meta:
        model = PracticeArea
        fields = ['icon', 'title', 'description', 'button_text', 'button_url', 'order', 'is_active']
        labels = {
            'title': 'Başlık',
            'button_text': 'Buton Metni',
            'button_url': 'Buton URL',
            'order': 'Sıralama',
            'is_active': 'Aktif'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LawyerForm(ModelForm):
    description = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='Hakkında'
    )
    education = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='Eğitim Bilgileri'
    )
    
    class Meta:
        model = Lawyer
        fields = ['name', 'surname', 'title', 'image', 'description', 'education', 
                 'experience', 'email', 'phone', 'linkedin', 'twitter', 'facebook', 
                 'instagram', 'order', 'is_active']
        labels = {
            'name': 'Ad',
            'surname': 'Soyad',
            'title': 'Ünvan',
            'image': 'Fotoğraf',
            'experience': 'Deneyim (Yıl)',
            'email': 'E-posta',
            'phone': 'Telefon',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'order': 'Sıralama',
            'is_active': 'Aktif'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BlogPostForm(ModelForm):
    content = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='İçerik'
    )
    
    class Meta:
        model = BlogPost
        fields = ['image', 'category', 'title', 'content', 'author', 
                 'publish_date', 'is_active']
        labels = {
            'image': 'Kapak Görseli',
            'category': 'Kategori',
            'title': 'Başlık',
            'author': 'Yazar',
            'publish_date': 'Yayın Tarihi',
            'is_active': 'Aktif'
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'data-nice-select': 'true'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContactInfoForm(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'email1', 'email2', 'phone1', 'phone2', 'map_url', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email1': forms.EmailInput(attrs={'class': 'form-control'}),
            'email2': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone1': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'map_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CaseStudyForm(ModelForm):
    summary = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Dava hakkında kısa bir özet yazın...'
        }),
        required=True,
        label='Özet'
    )

    content = forms.CharField(
        widget=CKEditorWidget(
            config_name='default',
            attrs={'class': 'form-control', 'style': 'width:100%;'}
        ),
        required=True,
        label='Detaylı Açıklama'
    )

    result = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Dava sonucunu yazın...'
        }),
        required=False,
        label='Sonuç'
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Başlangıç Tarihi'
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False,
        label='Bitiş Tarihi'
    )

    class Meta:
        model = CaseStudy
        fields = [
            'title', 'case_type', 'status', 'client_type',
            'summary', 'content', 'result',
            'start_date', 'end_date',
            'featured_image',
            'is_featured', 'is_public', 'order',
            'meta_title', 'meta_description'
        ]
        labels = {
            'title': 'Dava Başlığı',
            'case_type': 'Dava Türü',
            'status': 'Durum',
            'client_type': 'Müvekkil Türü',
            'featured_image': 'Kapak Görseli',
            'is_featured': 'Öne Çıkan Dava',
            'is_public': 'Yayında',
            'order': 'Sıralama',
            'meta_title': 'Meta Başlık',
            'meta_description': 'Meta Açıklama'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dava başlığını girin...'
            }),
            'case_type': forms.Select(attrs={
                'class': 'form-control',
                'data-nice-select': 'true'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'data-nice-select': 'true'
            }),
            'client_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Örn: Bireysel, Kurumsal'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO başlığı girin...'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'SEO açıklaması girin...'
            })
        }
        help_texts = {
            'meta_title': 'Sayfa başlığı (SEO için)',
            'meta_description': 'Sayfa açıklaması (SEO için, en fazla 160 karakter)',
            'is_featured': 'Bu dava ana sayfada öne çıkarılsın mı?',
            'is_public': 'Bu dava yayında olsun mu?',
            'client_type': 'Örn: Bireysel, Kurumsal, KOBİ, vb.',
            'order': 'Sıralama önceliği (küçük sayı = üst sıra)'
        }

    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError('Meta açıklama en fazla 160 karakter olmalıdır.')
        return meta_description

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('Bitiş tarihi başlangıç tarihinden önce olamaz.')

        return cleaned_data 