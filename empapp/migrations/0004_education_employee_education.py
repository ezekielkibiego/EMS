# Generated by Django 4.2.1 on 2023-06-22 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empapp', '0003_department_role_employee_address_employee_bonus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=100)),
                ('completion_year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='education',
            field=models.ManyToManyField(to='empapp.education'),
        ),
    ]
