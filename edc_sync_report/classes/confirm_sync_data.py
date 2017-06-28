from django.apps import apps as django_apps

from edc_sync_report.classes.confirmation_file import ConfirmationFile


class ConfirmSyncData:

    file_reader = ConfirmationFile

    def __init__(self, filename=None, *args, **kwargs):
        self.filename = filename
        self.missing_records = []
        self.is_synchronized = self.verify()

    def verify(self):
        is_verify = True
        for row in self.file_reader(filename=self.filename).read():
            label_lower, options = row
            model = django_apps.get_model(*label_lower)
            try:
                model.objects.get_by_natural_key(*options)
            except model.DoesNotExist:
                is_verify = False
                self.missing_records.append(row)
        return is_verify


class ConfirmSubjectConsentData(ConfirmSyncData):

    def __init__(self, consent_model=None, filename=None, *args, **kwargs):
        super().__init__(filename=filename)
        self.missing_records = []
        self.consent_model = consent_model
        self.is_synchronized = self.verify()

    def verify(self):
        for options in self.file_reader(filename=self.filename).read():
            is_synchronized = True
            try:
                self.consent_model.objects.get_by_natural_key(
                    *options.get(self.consent_model._meta.label_lower))
            except self.consent_model.DoesNotExist:
                is_synchronized = False
                self.missing_records.append(options)
        return is_synchronized


class ConfirmSubjectVisitData(ConfirmSyncData):

    def __init__(self, subject_visit=None, filename=None, *args, **kwargs):
        super().__init__(filename=filename)
        self.missing_records = []
        self.subject_visit = subject_visit
        self.is_synchronized = self.verify()

    def verify(self):
        is_synchronized = True
        for row in self.file_reader(filename=self.filename).read():
            try:
                self.subject_visit.objects.get_by_natural_key(
                    *row.get(self.subject_visit._meta.label_lower))
            except self.subject_visit.DoesNotExist:
                is_synchronized = False
                self.missing_records.append(row)
        return is_synchronized
