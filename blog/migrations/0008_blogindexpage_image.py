# Generated by Django 3.1.4 on 2020-12-21 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('blog', '0007_blogpage_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image'),
            preserve_default=False,
        ),
    ]
