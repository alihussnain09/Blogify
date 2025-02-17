# Generated by Django 5.1 on 2024-08-22 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_blog_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blogs.category'),
        ),
    ]
