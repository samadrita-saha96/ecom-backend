# Generated by Django 3.0.5 on 2020-06-17 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=70)),
                ('category_image', models.ImageField(blank=True, upload_to='category-img')),
                ('category_description', models.TextField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
        migrations.CreateModel(
            name='Sub_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category')),
            ],
            options={
                'verbose_name_plural': 'sub-category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_desc_short', models.TextField()),
                ('product_desc_long', models.TextField()),
                ('img1', models.ImageField(upload_to='product_img/img1')),
                ('img2', models.ImageField(blank=True, upload_to='product_img/img2')),
                ('img3', models.ImageField(blank=True, upload_to='product_img/img3')),
                ('price', models.FloatField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category')),
            ],
            options={
                'verbose_name_plural': 'Product',
            },
        ),
    ]
