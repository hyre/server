# Generated by Django 3.1.2 on 2020-10-30 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201029_1332'),
        ('company', '0002_auto_20201029_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='user.dev'),
        ),
    ]
