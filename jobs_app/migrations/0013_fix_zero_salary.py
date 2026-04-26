from django.db import migrations

def fix_zero_salary(apps, schema_editor):
    JobListing = apps.get_model('jobs_app', 'JobListing')
    JobListing.objects.filter(salary__lte=0).update(salary=1)

class Migration(migrations.Migration):
    dependencies = [
        ('jobs_app', '0012_alter_joblisting_salary_and_more'),
    ]
    operations = [
        migrations.RunPython(fix_zero_salary),
    ]