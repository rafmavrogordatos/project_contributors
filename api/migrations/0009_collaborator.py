# Generated by Django 5.1.6 on 2025-02-12 20:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_collaborators_project_active_collaborators'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='api.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('project', 'user'), name='unique_collaboration')],
            },
        ),
    ]
