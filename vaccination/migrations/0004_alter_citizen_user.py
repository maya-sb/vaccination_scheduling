# Generated by Django 3.2.3 on 2021-06-01 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccination', '0003_auto_20210531_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='citizen', to=settings.AUTH_USER_MODEL),
        ),
    ]
