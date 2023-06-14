# Generated by Django 4.2.1 on 2023-06-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]