# Generated by Django 5.1.6 on 2025-02-28 09:27

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ad')),
                ('surname', models.CharField(max_length=100, verbose_name='Soyad')),
                ('title', models.CharField(help_text='Örn: Avukat, Stajyer Avukat', max_length=100, verbose_name='Ünvan')),
                ('image', models.ImageField(upload_to='lawyers/', verbose_name='Fotoğraf')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Hakkında')),
                ('education', ckeditor.fields.RichTextField(verbose_name='Eğitim Bilgileri')),
                ('experience', models.PositiveIntegerField(verbose_name='Deneyim (Yıl)')),
                ('email', models.EmailField(max_length=254, verbose_name='E-posta')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Telefon')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn')),
                ('twitter', models.URLField(blank=True, verbose_name='Twitter')),
                ('facebook', models.URLField(blank=True, verbose_name='Facebook')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram')),
                ('order', models.IntegerField(default=0, verbose_name='Sıralama')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Mi?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Avukat',
                'verbose_name_plural': 'Avukatlar',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='LawyerCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Sertifika Adı')),
                ('institution', models.CharField(max_length=200, verbose_name='Veren Kurum')),
                ('date', models.DateField(verbose_name='Alınma Tarihi')),
                ('description', models.TextField(blank=True, verbose_name='Açıklama')),
                ('image', models.ImageField(blank=True, upload_to='certificates/', verbose_name='Sertifika Görseli')),
                ('order', models.IntegerField(default=0, verbose_name='Sıralama')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Mi?')),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='webui.lawyer', verbose_name='Avukat')),
            ],
            options={
                'verbose_name': 'Sertifika',
                'verbose_name_plural': 'Sertifikalar',
                'ordering': ['order', '-date'],
            },
        ),
        migrations.CreateModel(
            name='LawyerExpertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_years', models.PositiveIntegerField(verbose_name='Bu Alandaki Deneyim (Yıl)')),
                ('description', models.TextField(blank=True, verbose_name='Açıklama')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Ana Uzmanlık Alanı Mı?')),
                ('order', models.IntegerField(default=0, verbose_name='Sıralama')),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expertise_areas', to='webui.lawyer', verbose_name='Avukat')),
                ('practice_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webui.practicearea', verbose_name='Uzmanlık Alanı')),
            ],
            options={
                'verbose_name': 'Avukat Uzmanlık Alanı',
                'verbose_name_plural': 'Avukat Uzmanlık Alanları',
                'ordering': ['order'],
                'unique_together': {('lawyer', 'practice_area')},
            },
        ),
    ]
