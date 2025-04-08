from django.db import models
from django.core.exceptions import ValidationError

class Kategoriya(models.Model):
    ady = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Kategoriyalar"
    def __str__(self):
        return self.ady
class Onum(models.Model):
    ady = models.CharField(max_length=100)
    kategoriya=models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    baha = models.DecimalField(max_digits=10, decimal_places=2)
    suraty = models.ImageField(upload_to='media/images/', blank=True, null=True)

    def __str__(self):
        return self.ady

    class Meta:
        verbose_name_plural = "Onumler"

class Alyjy(models.Model):
    ady = models.CharField(max_length=100)
    yurt = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Alyjylar"

    def __str__(self):
        return self.ady

class Ammar(models.Model):
    onum = models.OneToOneField(Onum, on_delete=models.CASCADE)
    mukdary = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.onum.ady} - {self.mukdary} kg"

    class Meta:
        verbose_name_plural = "Ammar"

class ImportHasabat(models.Model):
    onum = models.ForeignKey(Onum, on_delete=models.CASCADE)
    mukdary = models.PositiveIntegerField()
    baha = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    senesi = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Import Hasabatlar"

    def save(self, *args, **kwargs):
        ammar, created = Ammar.objects.get_or_create(
            onum=self.onum,
            defaults={"mukdary": 0, "yerlesyan_yeri": "Belli däl"}
        )
        ammar.mukdary += self.mukdary
        ammar.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Import: {self.onum.ady} - {self.mukdary} kg"

class EksportSargyt(models.Model):
    onum = models.ForeignKey(Onum, on_delete=models.CASCADE)
    mukdary = models.PositiveIntegerField()
    partner = models.ForeignKey(Alyjy, on_delete=models.CASCADE)
    senesi = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Eksport Sargytlar"
        
    def __str__(self):
        return f"Eksport: {self.onum.ady} - {self.mukdary} kg"   

    def save(self, *args, **kwargs):
        MIN_LOCAL_STOCK = 100  # kg

        try:
            ammar = Ammar.objects.get(onum=self.onum)
        except Ammar.DoesNotExist:
            raise ValidationError("Ammarda bu önüm ýok.")

        if ammar.mukdary - self.mukdary < MIN_LOCAL_STOCK:
            raise ValidationError("Eksport üçin ýeterlik önüm ýok! Içerki bazar üpjün edilmeli.")

        ammar.mukdary -= self.mukdary
        ammar.save()
        super().save(*args, **kwargs)

class Sargyt(models.Model):
    müşderi_ady = models.CharField(max_length=100)
    ýer = models.CharField(max_length=100)
    onum = models.ForeignKey(Onum, on_delete=models.CASCADE)
    mukdary = models.PositiveIntegerField()
    baha = models.DecimalField(max_digits=10, decimal_places=2)
    senesi = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.müşderi_ady} - {self.onum.ady}"
    
    class Meta:
        verbose_name_plural = "Sargytlar"
