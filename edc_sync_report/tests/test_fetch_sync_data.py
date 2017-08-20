import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag

from ..classes import FetchSyncData, SyncSite, SyncConnectionError


@tag('fetch')
class TestFetchSyncReportData(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestFetchSyncReportData, cls).setUpClass()

    def test_fetch_sync_data_no_connection(self):
        site = SyncSite(name='test-site', url='http://localhost:8000/')
        fetched_data = FetchSyncData(site=site)
        self.assertRaises(SyncConnectionError, fetched_data.data)

    def test_fetch_sync_data_with_connection(self):
        site = SyncSite(name='test-site', url='http://localhost:8000/')
        fetched_data = FetchSyncData(site=site)
        self.assertRaises(fetched_data.data())
