from django import forms


class SearchForm(forms.Form):
    """ Класс формы поиска """
    query = forms.CharField(max_length=100,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control me-2 mx-1',
                                    'placeholder': 'Введите запрос',
                                }
                            ))

    def clean_query(self):
        """
        Переопределённый метод очистки поля query.
        Удаляет лишние пробелы внутри текста.
        """
        query = self.cleaned_data['query']
        cleaned_query = " ".join(query.split())
        return cleaned_query
