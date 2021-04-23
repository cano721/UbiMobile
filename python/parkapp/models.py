from django.db import models

# Create your models here.
class Parking_floor(models.Model):
    p_id = models.AutoField(db_column='p_id', primary_key=True)
    pf_floor = models.IntegerField(db_column='pf_floor')
    pf_space = models.IntegerField(db_column='pf_space')
    pf_data = models.IntegerField(db_column='pf_data')

    class Meta:
        managed = False
        db_table = 'parking_floor'

    def __str__(self):
        return str(self.p_id) + ' ' + str(self.pf_floor) + ' ' + str(self.pf_space) + ' ' + str(self.pf_data) + ' ';