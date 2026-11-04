from django import forms

from .models import DemandeService


class DemandeServiceForm(forms.ModelForm):
    class Meta:
        model = DemandeService
        fields = (
            "nom_demandeur",
            "email_demandeur",
            "telephone_demandeur",
            "motif",
            "piece_jointe",
        )
        widgets = {
            "motif": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["piece_jointe"].required = False
        self.fields["piece_jointe"].help_text = (
            "Facultatif. Formats acceptés : PDF, JPG ou PNG (5 Mo maximum)."
        )
        self.fields["nom_demandeur"].required = True
        self.fields["email_demandeur"].required = True
        self.fields["telephone_demandeur"].required = True
        self.fields["motif"].required = True

    def clean_piece_jointe(self):
        fichier = self.cleaned_data.get("piece_jointe")
        if fichier and fichier.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Le fichier ne doit pas dépasser 5 Mo.")
        return fichier
