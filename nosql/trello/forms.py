from django import forms
from .models import Settings
from django.core.exceptions import ValidationError

from .TrelloToMongoAdapter import getDB
from .MongoDBUtility import getLists, getLabels, getMembers



class BoardForm(forms.Form):
    board = forms.TypedChoiceField(choices=(('Доска 1', 'Доска 1'), ('Доска 2', 'Доска 2'))) # тут надо достать все доски
    board.widget.attrs.update({'class': 'custom-select my-1 mr-2'})

    def save(self):
        return self.cleaned_data['board']


class ToLists:
    def __init__(self):
        db = getDB()
        self.Lists = []
        self.Labels = []
        self.Members = []
        tmp = getLists(db)
        for d in tmp:
            self.Lists.append((d['name'], d['name']))
        tmp = getLabels(db)
        for d in tmp:
            self.Labels.append(("{color},{name}".format(color=d['color'], name=d['name']),
                               "{color} ({name})".format(color=d['color'], name=d['name'])))
        tmp = getMembers(db)
        for d in tmp:
            self.Members.append(("{fullName},{username}".format(fullName=d['fullName'], username=d['username']),
                                "{fullName} ({username})".format(fullName=d['fullName'], username=d['username'])))

class SettingsForm(forms.Form):
    lists = ToLists()
    start_list = forms.TypedMultipleChoiceField(choices=lists.Lists)
    start_list.widget.attrs.update({'class': 'custom-select my-1 mr-2'})
    final_list = forms.TypedMultipleChoiceField(choices=lists.Lists)
    final_list.widget.attrs.update({'class': 'custom-select my-1 mr-2'})
    key_words = forms.CharField(required=False)
    key_words.widget.attrs.update({'class': 'form-control'})
    labels = forms.TypedMultipleChoiceField(choices=lists.Labels)
    labels.widget.attrs.update({'class': 'custom-select my-1 mr-2'})
    executors = forms.TypedMultipleChoiceField(choices=lists.Members)
    executors.widget.attrs.update({'class': 'custom-select my-1 mr-2'})
    attachment = forms.BooleanField(required=False)
    attachment.widget.attrs.update({'class': 'form-check-input'})
    comments = forms.BooleanField(required=False)
    comments.widget.attrs.update({'class': 'form-check-input'})
    from_date = None
    to_date = None
    due_date = None


    def save(self, due_date, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
        self.due_date = due_date
        new_settings = Settings(start_list=self.cleaned_data['start_list'],
                                final_list=self.cleaned_data['final_list'],
                                key_words=self.cleaned_data['key_words'].split(' '),
                                labels=self.cleaned_data['labels'],
                                executors=self.cleaned_data['executors'],
                                due_date=due_date,
                                from_date=from_date,
                                to_date=to_date,
                                attachment=self.cleaned_data['attachment'],
                                comments=self.cleaned_data['comments'])
        return new_settings