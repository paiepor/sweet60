from django.db import migrations

def convert_salary(apps, schema_editor):
    JobListing = apps.get_model('jobs_app', 'JobListing')
    for job in JobListing.objects.all():
        try:
            cleaned = str(job.salary).replace(',', '').strip()
            job.salary = int(float(cleaned))
            job.save()
        except (ValueError, TypeError):
            job.salary = 0
            job.save()

class Migration(migrations.Migration):
    dependencies = [
        ('jobs_app', '0010_remove_userprofile_avatar_userprofile_avatar_b64'),
    ]
    operations = [
        migrations.RunPython(convert_salary),
    ]