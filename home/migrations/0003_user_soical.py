# Generated by Django 4.2.3 on 2023-07-17 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_post_options_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_soical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
