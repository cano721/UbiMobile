from django.db import models

# Create your models here.
class Users_car(models.Model):
    uc_id = models.AutoField(db_column='uc_id', primary_key=True)
    u_id = models.CharField(db_column='u_id', max_length=20)
    uc_model = models.CharField(db_column='uc_model', max_length=20)
    uc_number = models.CharField(db_column='uc_number', max_length=10)
    uc_color = models.CharField(db_column='uc_color', max_length=10)
    uc_distance = models.IntegerField(db_column='uc_distance')
    uc_repair = models.DateField(db_column='uc_repair')
    uc_age = models.CharField(db_column='uc_age', max_length=4)

    class Meta:
        managed = False
        db_table = 'users_car'

    def __str__(self):
        return str(self.uc_id) + ' ' + self.u_id + ' ' + self.uc_model + ' ' + self.uc_number + ' '\
               + self.uc_color + ' ' + str(self.uc_distance) + ' ' + str(self.uc_repair) + ' ' + str(self.uc_age) + ' ';


class Parking_floor(models.Model):
    pf_id = models.AutoField(db_column='pf_id', primary_key=True)
    u_id = models.CharField(db_column='u_id', max_length=20)
    p_id = models.IntegerField(db_column='p_id')
    pf_floor = models.IntegerField(db_column='pf_floor')
    pf_space = models.IntegerField(db_column='pf_space')
    pf_data = models.IntegerField(db_column='pf_data')

    class Meta:
        managed = False
        db_table = 'parking_floor'

    def __str__(self):
        return str(self.pf_id) + ' ' + self.u_id + ' ' + str(self.p_id) + ' ' + str(self.pf_floor) + ' ' + str(
            self.pf_space) + ' ' + str(self.pf_data) + ' ';

class Users_car_ac(models.Model):
    uca_id = models.AutoField(db_column='uca_id', primary_key=True)
    uc_id = models.IntegerField(db_column='uc_id')
    u_id = models.CharField(db_column='u_id', max_length=20)
    uc_number = models.CharField(db_column='uc_number', max_length=10)
    uca_date = models.DateField(db_column='uca_date')
    uca_pulse = models.IntegerField(db_column='uca_pulse')

    class Meta:
        managed = False
        db_table = 'users_car_ac'

    def __str__(self):
        return str(self.uca_id) + ' ' + str(self.uc_id) + ' ' + self.u_id + ' ' + self.uc_number + ' '\
               + str(self.uca_date) + ' ' + str(self.uca_pulse) + ' ';