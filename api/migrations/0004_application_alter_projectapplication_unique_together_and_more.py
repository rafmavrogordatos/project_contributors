# Generated by Django 5.1.6 on 2025-02-12 15:33

import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_password'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='projectapplication',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='projectapplication',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='projectapplication',
            name='project',
        ),
        migrations.AlterUniqueTogether(
            name='projectcollaborator',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='projectcollaborator',
            name='collaborator',
        ),
        migrations.RemoveField(
            model_name='projectcollaborator',
            name='project',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='active_collaborators',
            new_name='collaborators',
        ),
        migrations.RemoveField(
            model_name='project',
            name='completed',
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.user'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='max_collaborators',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='skill',
            name='language',
            field=models.CharField(choices=[('C++', 'C++'), ('Javascript', 'Javascript'), ('Python', 'Python'), ('Java', 'Java'), ('Lua', 'Lua'), ('Rust', 'Rust'), ('Go', 'Go'), ('Julia', 'Julia')], max_length=20),
        ),
        migrations.AlterField(
            model_name='skill',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('experienced', 'Experienced'), ('expert', 'Expert')], max_length=20),
        ),
        migrations.AlterField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='api.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='residence',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.AddConstraint(
            model_name='skill',
            constraint=models.UniqueConstraint(fields=('user', 'language'), name='unique_user_skill'),
        ),
        migrations.AddField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='api.user'),
        ),
        migrations.AddField(
            model_name='application',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='api.project'),
        ),
        migrations.DeleteModel(
            name='ProjectApplication',
        ),
        migrations.DeleteModel(
            name='ProjectCollaborator',
        ),
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(fields=('applicant', 'project'), name='unique_application'),
        ),
    ]
