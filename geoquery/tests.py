# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Used for testing views.
from django.test import Client
from django.urls import reverse
from django.utils.http import urlencode


class TestGeoqueryViews(TestCase):
    """The following unit tests validate that query views execute as expected.
        The unit tests follow the explanation given in the django tutorial listed below with modifications relevant to our query form setup.

        https://docs.djangoproject.com/en/2.0/intro/tutorial05/#test-a-view
    """

    def test_lookup_success_view(self):
        #  create the client simulator
        client = Client()

        #  fake form data by building a query parameter string 
        #  using a dictionary giving location=1314+chavez+st%2C+las+vegas%2C+nm
        query_str = urlencode({'location':'1314 chavez st, las vegas, nm'})
        
        #  build a complete url pattern from named pattern, 'lookup'. See geopydemo/urls.py
        #  then append the query parameter string
        #  should give: /lookup/?location=1314+chavez+st%2C+las+vegas%2C+nm
        url = reverse('lookup') + '?' + query_str
        
        #  fake a client request to url and get response object (what is sent to browser from the associated view)
        response = client.get(url)

        #  Grab the context variable known as 'result'. See geoquery/views.py
        result_var = response.context['result']

        #  Verify that the result represents a match - a match was found for the given address...    
        self.assertNotEqual(result_var, 'Location not found in Nominatim')

    def test_lookup_failure_view(self):
        client = Client()
        query_str = urlencode({'location':'1314 cha st, las vegas, nm'})
        url = reverse('lookup') + '?' + query_str
        response = client.get(url)
        result_var = response.context['result']

        #  Verify that the result represents a failed search - no match found for the given addresss.
        self.assertEqual(result_var, 'Location not found in Nominatim')

    def test_lookup_distance_view(self):
        client = Client()
        query_str = urlencode({'location':'1314 chavez st, las vegas, nm'})
        url = reverse('distance') + '?' + query_str
        response = client.get(url)
        result_var = response.context['result']

        #  Verify that result is a distance between .4 and .5 (e.g., 0.445227747111)    
        self.assertEqual(result_var > .4 and result_var < .5, True)
