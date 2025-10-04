from django.db import models
from datetime import date

# -------------------------------
# 1. Osztaly
# -------------------------------
class Osztaly(models.Model):
    evfolyam = models.IntegerField()
    betu = models.CharField(max_length=1)
    terem = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('evfolyam', 'betu', 'terem')

    def __str__(self):
        return f"{self.evfolyam}.{self.betu} ({self.terem})"


# -------------------------------
# 2. Tanulo
# -------------------------------
class Tanulo(models.Model):
    nev = models.CharField(max_length=100)
    szul_hely = models.CharField(max_length=100)
    szul_ido = models.DateField()
    anyja_neve = models.CharField(max_length=100)
    lakcim = models.CharField(max_length=150)
    beiratkozas_ido = models.DateField()
    szak = models.CharField(max_length=50)
    osztaly = models.ForeignKey(Osztaly, on_delete=models.CASCADE, related_name="tanulok")
    kollegista = models.BooleanField(default=False)
    kollegium = models.CharField(max_length=50, blank=True)
    
    naplo_sorszam = models.IntegerField(blank=True, null=True)
    torzslapszam = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Napló és törzslap generálása osztályonként
        if self.naplo_sorszam is None:
            tanulok_osztaly = Tanulo.objects.filter(osztaly=self.osztaly)
            szeptember1 = date(self.beiratkozas_ido.year, 9, 1)
            if self.beiratkozas_ido < szeptember1:
                # névsorrend
                sorszam = list(tanulok_osztaly.order_by('nev')).index(self) + 1 if self.id else tanulok_osztaly.count() + 1
            else:
                # beiratkozás sorrendje
                sorszam = tanulok_osztaly.count() + 1
            self.naplo_sorszam = sorszam
            self.torzslapszam = f"{self.naplo_sorszam}/{self.beiratkozas_ido.year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nev} ({self.osztaly})"


# -------------------------------
# 3. Tanar
# -------------------------------
class Tanar(models.Model):
    nev = models.CharField(max_length=100)
    tantargy = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nev} – {self.tantargy}"


# -------------------------------
# 4. Tantargy
# -------------------------------
class Tantargy(models.Model):
    nev = models.CharField(max_length=50)
    evfolyam = models.IntegerField()
    tipus_valasz = [
        ('kozismereti', 'Közismereti'),
        ('szakmai', 'Szakmai')
    ]
    tipus = models.CharField(max_length=20, choices=tipus_valasz)
    heti_oraszam = models.IntegerField()
    eves_oraszam = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # éves óraszám generálása szabályok alapján
        if self.evfolyam in [9, 10, 11]:
            self.eves_oraszam = self.heti_oraszam * 36
        elif self.evfolyam == 12:
            if self.tipus == 'kozismereti':
                self.eves_oraszam = self.heti_oraszam * 31
            else:
                self.eves_oraszam = self.heti_oraszam * 36
        elif self.evfolyam == 13:
            self.eves_oraszam = self.heti_oraszam * 31
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nev} ({self.evfolyam})"


# -------------------------------
# 5. Ora
# -------------------------------
class Ora(models.Model):
    tanar = models.ForeignKey(Tanar, on_delete=models.CASCADE, related_name="orak")
    osztaly = models.ForeignKey(Osztaly, on_delete=models.CASCADE, related_name="orak")
    tantargy = models.ForeignKey(Tantargy, on_delete=models.CASCADE, related_name="orak")
    nap = models.CharField(max_length=10)
    ora = models.IntegerField()

    def __str__(self):
        return f"{self.osztaly} – {self.tantargy} ({self.nap} {self.ora}. óra)"


# -------------------------------
# 6. Jegy
# -------------------------------
class Jegy(models.Model):
    tanulo = models.ForeignKey(Tanulo, on_delete=models.CASCADE, related_name="jegyek")
    tantargy = models.ForeignKey(Tantargy, on_delete=models.CASCADE, related_name="jegyek")
    datum = models.DateField(auto_now_add=True)
    jegy = models.FloatField()
    tema = models.CharField(max_length=100, blank=True)
    szamonkeres_tipus = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.tanulo} – {self.tantargy}: {self.jegy}"

    class Meta:
        ordering = ['datum']
