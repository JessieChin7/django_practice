# Generated by Django 4.1 on 2022-09-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_page', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(null=True, upload_to='video/', verbose_name=''),
        ),
    ]
