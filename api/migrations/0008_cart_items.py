# Generated by Django 3.0.5 on 2020-06-29 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200623_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_img', models.CharField(max_length=255)),
                ('product_price', models.FloatField()),
                ('size', models.CharField(max_length=5)),
                ('quantity', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'unique_together': {('user', 'product_name', 'size')},
            },
        ),
    ]
