from django.apps import apps as django_apps
from datetime import datetime

from bcpp_subject.models import SubjectVisit, SubjectConsent
from bcpp_subject.sync_models import sync_models
from bcpp_subject.models.model_mixins import CrfModelMixin

from edc_sync_report.classes.verification_file import VerificationFile

class MismatchVerification(Exception):
    pass


class ExportVerificationJsonFile:

    file_writer = VerificationFile
    
    def __init__(self, survey=None, subject_identifiers=None,
                 community=None, verbose=None):
        self.survey = survey
        self.subject_identifiers = subject_identifiers
        self.community = community
        self.verbose = verbose

    def subject_consents_file(self):
        data = []
        subject_visits = SubjectVisit.objects.filter(
            survey=self.survey,
            subject_identifier__in=self.subject_identifiers)
        for subject_visit in subject_visits:
            subject_consent = SubjectConsent.objects.get(
                household_member=subject_visit.household_member)
            consent_filter = (
                subject_consent.subject_identifier,
                subject_consent.version,
                str(subject_consent.household_member.internal_identifier),
                subject_consent.household_member.household_structure.survey_schedule,
                subject_consent.household_member.household_structure.household.household_identifier,
                subject_consent.household_member.household_structure.household.plot.plot_identifier)
            data.append(
                {str(SubjectConsent._meta.label_lower): consent_filter})
        filename = '{}_consents_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))
    
    def subject_visits_file(self, ess_community=None):
        data = []
        subject_visits = SubjectVisit.objects.filter(
            survey=self.survey,
            subject_identifier__in=self.subject_identifiers)
        for visit in subject_visits:
            data.append(
                {str(SubjectVisit._meta.label_lower): visit.natural_key()})
        filename = '{}_subjectvisits_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))
        
    def is_ignored(self, label_lower):
        skip_models = [
            'bcpp_subject.subjectconsent', 'bcpp_subject.correctconsent']
        if not 'historical' in label_lower and  not label_lower in skip_models:
            return True
        return False
        
    def crfs_verification_file(self):
        data = []
        model_label_lowers = [
            label for label in sync_models if not self.is_ignored(label)]
        for subject_identifier in self.subject_identifiers:
            visit = SubjectVisit.objects.filter(
                survey=self.survey,
                subject_identifier=subject_identifier)
            temp_data = []
            for label_lower in model_label_lowers:
                model = django_apps.get_model(*label_lower.split('.'))
                try:
                    if issubclass(model, CrfModelMixin):
                        obj = model.objects.get(subject_visit=visit)
                    else:
                        try:
                            obj = model.objects.get(
                                subject_identifier=visit.subject_identifier)
                        except model.DoesNotExist:
                            print(model)
                    if obj:
                        temp_data.append(dict({str(model._meta.label_lower): obj.natural_key()}))
                except:
                    print(model)
            data.append(temp_data)
        filename = '{}_crfs_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))
