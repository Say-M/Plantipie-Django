# Generated by Django 4.2 on 2023-05-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_product_delete_plant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='additional_images',
            field=models.FileField(blank=True, null=True, upload_to='assets/images', verbose_name='Document'),
        ),
    ]
