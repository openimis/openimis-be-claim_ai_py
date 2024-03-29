# Generated by Django 3.0.14 on 2022-02-20 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claim_ai', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claimbundleevaluation',
            name='fhir_response',
        ),
        migrations.RemoveField(
            model_name='historicalclaimbundleevaluation',
            name='fhir_response',
        ),
        migrations.AlterField(
            model_name='claimprovisionevaluationresult',
            name='claim_evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluated_items', to='claim_ai.SingleClaimEvaluationResult'),
        ),
        migrations.AlterField(
            model_name='singleclaimevaluationresult',
            name='bundle_evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='claim_ai.ClaimBundleEvaluation'),
        ),
    ]
