from django import forms
from .models import Tanulo, Tantargy, Jegy

class TanuloForm(forms.ModelForm):
    class Meta:
        model = Tanulo
        fields = [
            "nev", "szul_hely", "szul_ido", "anyja_neve", "lakcim", "beiratkozas_ido",
            "szak", "osztaly", "kollegista", "kollegium"
        ]
        widgets = {
            "beiratkozas_ido": forms.DateInput(attrs={"type": "date"}),
            "szul_ido": forms.DateInput(attrs={"type": "date"}),
        }

class TantargyForm(forms.ModelForm):
    class Meta:
        model = Tantargy
        fields = ["nev", "evfolyam", "tipus", "heti_oraszam"]

class JegyForm(forms.ModelForm):
    class Meta:
        model = Jegy
        fields = ["tanulo", "tantargy", "jegy", "tema", "szamonkeres_tipus"]
