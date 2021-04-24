from django.db import models

# Create your models here.
class Users(models.Model):
    u_id = models.CharField(db_column='u_id', max_length=20, primary_key=True)
    u_gender = models.CharField(db_column='u_gender',max_length=10)
    u_pwd = models.CharField(db_column='u_pwd',max_length=20)
    u_name = models.CharField(db_column='u_name',max_length=20)
    u_age = models.IntegerField(db_column='u_age')
    u_email = models.CharField(db_column='u_email',max_length=50)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.u_id + ' ' + self.u_gender + ' ' + self.u_pwd + ' ' \
               + self.u_name + ' ' + str(self.u_age) + self.u_email + ' ';