# Generated by Django 4.1 on 2022-09-30 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_page', '0009_alter_photo_table_alter_video_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='upload_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='upload_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
