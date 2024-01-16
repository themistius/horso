# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Horses(models.Model):
    at = models.TextField(db_column='At', blank=True, null=True)  # Field name made lowercase.
    yas = models.TextField(db_column='Yas', blank=True, null=True)  # Field name made lowercase.
    ulkeadi = models.TextField(db_column='UlkeAdi', blank=True, null=True)  # Field name made lowercase.
    irkadi = models.TextField(db_column='IrkAdi', blank=True, null=True)  # Field name made lowercase.
    baba = models.TextField(db_column='Baba', blank=True, null=True)  # Field name made lowercase.
    anne = models.TextField(db_column='Anne', blank=True, null=True)  # Field name made lowercase.
    kosu = models.IntegerField(db_column='Kosu', blank=True, null=True)  # Field name made lowercase.
    birinci = models.IntegerField(db_column='Birinci', blank=True, null=True)  # Field name made lowercase.
    ikinci = models.IntegerField(db_column='Ikinci', blank=True, null=True)  # Field name made lowercase.
    ucuncu = models.IntegerField(db_column='Ucuncu', blank=True, null=True)  # Field name made lowercase.
    dorduncu = models.IntegerField(db_column='Dorduncu', blank=True, null=True)  # Field name made lowercase.
    besinci = models.IntegerField(db_column='Besinci', blank=True, null=True)  # Field name made lowercase.
    birinciyuzde = models.IntegerField(db_column='BirinciYuzde', blank=True, null=True)  # Field name made lowercase.
    ikinciyuzde = models.IntegerField(db_column='IkinciYuzde', blank=True, null=True)  # Field name made lowercase.
    ucuncuyuzde = models.IntegerField(db_column='UcuncuYuzde', blank=True, null=True)  # Field name made lowercase.
    dorduncuyuzde = models.IntegerField(db_column='DorduncuYuzde', blank=True, null=True)  # Field name made lowercase.
    besinciyuzde = models.IntegerField(db_column='BesinciYuzde', blank=True, null=True)  # Field name made lowercase.
    kazanc = models.TextField(db_column='Kazanc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'horses'


class Jockeys(models.Model):
    jokey = models.TextField(db_column='Jokey', blank=True, null=True)  # Field name made lowercase.
    koşu = models.TextField(db_column='Koşu', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    number_1_field = models.TextField(db_column='1.', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    number_2_field = models.TextField(db_column='2.', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    number_3_field = models.TextField(db_column='3.', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    number_4_field = models.TextField(db_column='4.', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    number_5_field = models.TextField(db_column='5.', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    number_1_field_0 = models.TextField(db_column='1.%', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier. Field renamed because of name conflict.
    number_2_field_0 = models.TextField(db_column='2.%', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier. Field renamed because of name conflict.
    number_3_field_0 = models.TextField(db_column='3.%', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier. Field renamed because of name conflict.
    number_4_field_0 = models.TextField(db_column='4.%', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier. Field renamed because of name conflict.
    number_5_field_0 = models.TextField(db_column='5.%', db_collation='NOCASE', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier. Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'jockeys'


class Races(models.Model):
    city = models.TextField(db_column='City', db_collation='NOCASE,', blank=True, null=True)  # Field name made lowercase.
    race_time = models.TextField(db_column='Race Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    at_i_smi = models.TextField(db_column='At İsmi', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    yaş = models.TextField(db_column='Yaş', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    orijin_baba_anne_field = models.TextField(db_column='Orijin(Baba - Anne)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sıklet = models.TextField(db_column='Sıklet', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    jokey = models.TextField(db_column='Jokey', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    sahip = models.TextField(db_column='Sahip', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    antrenör = models.TextField(db_column='Antrenör', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    st = models.TextField(db_column='St', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    hp = models.TextField(db_column='HP', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    son_6_y_field = models.TextField(db_column='Son 6 Y.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    kgs = models.TextField(db_column='KGS', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    s20 = models.TextField(db_collation='NOCASE', blank=True, null=True)
    en_i_yi_d_field = models.TextField(db_column='En İyi D.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    gny = models.TextField(db_column='Gny', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.
    agf = models.TextField(db_column='AGF', db_collation='NOCASE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'races'
