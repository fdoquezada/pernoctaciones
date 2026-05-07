from django import forms

class UploadExcelForm(forms.Form):  # <--- Asegúrate de que se llame así
    archivo_excel = forms.FileField(
        label="Seleccionar archivo Excel",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )