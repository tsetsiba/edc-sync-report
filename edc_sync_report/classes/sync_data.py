from django.apps import apps as django_apps

from bcpp_subject.models import SubjectConsent, SubjectVisit
from .verification_file import VerificationFile


class VerifySyncData:
    
    file_reader = VerificationFile

    def __init__(self, filename=None, *args, **kwargs):
        self.filename = filename
        self.missing = []
        self.is_synchronized = self.verify()
    
    def verify(self):
        pass
    

class VerifySubjectConsentData(VerifySyncData):
    
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(filename=filename)
        self.missing = []
        self.is_synchronized = self.verify()

    def verify(self):
        is_synchronized = True
        for options in self.file_reader(filename=self.filename).read():
            try:
                SubjectConsent.objects.get_by_natural_key(
                    *options.get(SubjectConsent._meta.label_lower))
            except SubjectConsent.DoesNotExist:
                is_synchronized = False
                self.missing.append(options)
        return is_synchronized


class VerifySubjectVisitData(VerifySyncData):
    
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(filename=filename)
        self.missing = []
        self.is_synchronized = self.verify()
        
    def verify(self):
        is_synchronized = True
        for row in self.file_reader(filename=self.filename).read():
            try:
                SubjectVisit.objects.get_by_natural_key(
                    *row.get(SubjectVisit._meta.label_lower))
            except SubjectVisit.DoesNotExist:
                is_synchronized = False
                self.missing.append(row)
        return is_synchronized


class VerifyCrfsData(VerifySyncData):
    
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(filename=filename)
        self.missing = []
        self.is_synchronized = self.verify()
    
    def verify(self):
        is_synchronized = True
        for row in self.file_reader(filename=self.filename).read():
            label_lower, options = row
            model = django_apps.get_model(*label_lower)
            try:
                model.objects.get_by_natural_key(*options)
            except model.DoesNotExist:
                is_synchronized = False
                self.missing.append(row)
        return is_synchronized
