from test_base import MainTestCase
import os
from odk_viewer.models import ParsedInstance, DataDictionary
from django.core.urlresolvers import reverse
import odk_viewer


class TestGPS(MainTestCase):

    def test_gps(self):
        self._create_user_and_login()
        self._publish_survey()
        self._make_submissions()
        self._check_has_geopoints()
        self._check_link_to_map_view()
        self._check_lat_lng()
        self._check_map_view()

    def _publish_survey(self):
        self.this_directory = os.path.dirname(__file__)
        xls_path = os.path.join(self.this_directory, "fixtures", "gps", "gps.xls")
        MainTestCase._publish_xls_file(self, xls_path)

    def _make_submissions(self):
        surveys = ['gps_1980-01-23_20-52-08',
                   'gps_1980-01-23_21-21-33',]
        for survey in surveys:
            path = os.path.join(self.this_directory, 'fixtures', 'gps', 'instances', survey + '.xml')
            self._make_submission(path)

    def _check_has_geopoints(self):
        self.assertEqual(DataDictionary.objects.count(), 1)
        dd = DataDictionary.objects.all()[0]
        self.assertTrue(dd.has_surveys_with_geopoints())

    def _check_link_to_map_view(self):
        response = self.client.get("/")
        map_url = '<a href="/odk_viewer/map/gps/">map</a>'
        self.assertTrue(map_url in response.content)

    def _check_lat_lng(self):
        expected_values = [
            (40.81101715564728, -73.96446704864502),
            (40.811086893081665, -73.96449387073517),
            ]
        for pi, lat_lng in zip(ParsedInstance.objects.all(), expected_values):
            self.assertEquals(pi.lat, lat_lng[0])
            self.assertEquals(pi.lng, lat_lng[1])

    def _check_map_view(self):
        map_url = reverse(odk_viewer.views.map, kwargs={'id_string': 'gps'})
        response = self.client.get(map_url)
        # testing the response context to get a concise notification
        # if the lat/long values have changed.
        expected_ll = '{"lat": 40.811052024364471, "lng": -73.964480459690094}'
        for r in response.context:
            self.assertEqual(expected_ll, r.center)
        html_path = os.path.join(self.this_directory, 'fixtures', 'gps', 'map.html')
        with open(html_path) as f:
            expected_content = f.read()
        self.assertEqual(expected_content, response.content)