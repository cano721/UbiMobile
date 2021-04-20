from django.db import models

# Create your models here.
class Parking(models.Model):
    p_id = models.AutoField(db_column='p_id', primary_key=True)
    u_id = models.CharField(db_column='u_id',max_length=20)
    p_name = models.CharField(db_column='p_name',max_length=20)
    p_addr = models.CharField(db_column='p_addr',max_length=100)
    p_cap = models.IntegerField(db_column='p_cap')

    class Meta:
        managed = False
        db_table = 'parking'

    def __str__(self):
        return str(self.p_id) + ' ' + self.u_id + ' ' + self.p_name + ' ' + self.p_addr + ' ' + str(self.p_cap) + ' ';