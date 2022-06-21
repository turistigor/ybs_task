from django.db import models

import prices_comparator.common as const


class ImportModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=const.IMPORT_UNIT_NAME_MAX_LENGTH)
    date = models.DateTimeField()
    parent_id = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    type = models.CharField(choices=const.IMPORT_UNIT_TYPE_CHOICES),
    price = models.PositiveBigIntegerField(blank=True, null=True)
