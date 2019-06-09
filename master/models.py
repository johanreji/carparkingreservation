from django.db import models
import PIL
import time

# Create your models here.

def user_directory_path(instance, filename):
  try:
    id=ParkingAreas.objects.latest('area_id')
    return 'areas/{0}.jpg'.format(str(id))
  except Exception:
    id=0
    return 'areas/{0}.jpg'.format(str(id))	

class ParkingAreas(models.Model):
	height = models.IntegerField(null=True)
	width = models.IntegerField(null=True)
	area_id = models.AutoField(primary_key=True)
	area_name = models.CharField(max_length=20, null=True)
	area_image = models.ImageField(upload_to=user_directory_path, height_field='height', width_field='width')
	row_count = models.IntegerField(null=True)
	column_count = models.IntegerField(null=True)
	is_active = models.BooleanField(default=False)

class SlotDims(models.Model):
	slot_id = models.AutoField(primary_key=True)
	area_id = models.ForeignKey(
        'ParkingAreas',related_name="area",
        on_delete=models.CASCADE,
    )
	x_left = models.IntegerField()
	y_left = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()
	row = models.IntegerField()
	column = models.IntegerField()
	updated = models.BooleanField(default=False)

class RenderDims(models.Model):
	slot_id = models.IntegerField(primary_key=True)
	x_left = models.IntegerField()
	y_left = models.IntegerField()
	





