from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import uuid
import re
from django.core.exceptions import ValidationError


# バリデータの定義
def validate_date_format(value):
    if not re.match(r'\A\d{4}-\d{2}-\d{2}\z', value.strftime('%Y-%m-%d')):
        raise ValidationError("Invalid date format. It should be YYYY-MM-DD.")

class User(AbstractUser):
    birth = models.DateField(validators=[validate_date_format])

class Gmap(models.Model):

    class Meta:
        db_table = 'gmap'

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=25)
    comment = models.TextField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.ImageField(upload_to='images/')
    # image_url = models.URLField(max_length=200)
    magic_word = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gmaps')


    def save(self, *args, **kwargs):
        if self.magic_word:
            self.magic_word = hashlib.md5(self.magic_word.encode()).hexdigest()
        else:
            self.magic_word = ""
        super().save(*args, **kwargs)
