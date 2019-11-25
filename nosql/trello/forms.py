from django import forms
from .models import Link, Settings

from .TrelloToMongoAdapter import getDB
from .MongoDBUtility import getLists, getLabels, getMembers

class LinkForm(forms.Form):
    link = forms.URLField()

    link.widget.attrs.update({'class': 'form-control'})

    def save(self):
        # Тут наверное неплохо было бы проверить ссылочку
        new_link = Link(link=self.cleaned_data['link'])
        return new_link


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
    due_date = forms.DateField(required=False)
    due_date.widget.attrs.update({'class': 'form-control'})
    from_date = forms.DateField(required=False)
    from_date.widget.attrs.update({'class': 'form-control'})
    to_date = forms.DateField(required=False)
    to_date.widget.attrs.update({'class': 'form-control'})
    attachment = forms.BooleanField(required=False)
    attachment.widget.attrs.update({'class': 'form-check-input'})
    comments = forms.BooleanField(required=False)
    comments.widget.attrs.update({'class': 'form-check-input'})

    def save(self):
        # тут нужно проверить что даты до и после нормальные
        print(self.cleaned_data['start_list'])
        new_settings = Settings(start_list=self.cleaned_data['start_list'],
                                final_list=self.cleaned_data['final_list'],
                                key_words=self.cleaned_data['key_words'],
                                labels=self.cleaned_data['labels'],
                                executors=self.cleaned_data['executors'],
                                due_date=self.cleaned_data['due_date'],
                                from_date=self.cleaned_data['from_date'],
                                to_date=self.cleaned_data['to_date'],
                                attachment=self.cleaned_data['attachment'],
                                comments=self.cleaned_data['comments'])
        return new_settings