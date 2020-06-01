from django.test import TestCase
from django.urls import reverse
from kennywoodapi.models import Itinerary, Customer, Attraction, ParkArea
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import unittest


class TestAttractions(TestCase):
    def setUp(self):
        self.username = 'TestUser'
        self.password = 'Test123'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, family_members=9)

    def testPostAttraction(self):
        # Have to create a new park area 
        # so we can reference one when making an itinerary
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        # Then create an itinerary
        new_attraction = {
            "name": "ATTRACTION",
            "area_id": 1
        }

        response = self.client.post(
            reverse('attraction-list'), new_attraction, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Attraction.objects.count(), 1)

        self.assertEqual(Attraction.objects.get().name, new_attraction["name"])
    
    def testGetAttraction(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )

        response = self.client.get(
            reverse('attraction-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["name"], new_attraction.name)

        self.assertIn(new_attraction.name.encode(), response.content)
        
    def testDeleteAttraction(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )

        response = self.client.delete(
            reverse('attraction-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('attraction-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)
        
    def testEditAttraction(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
            
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )
        
        # Create new updated parkare.
        updated_attraction = {
            "name": "Updated Test Attraction",
            "area_id": 1
        }

        # Update the attraction in the db
        response = self.client.put(
            reverse('attraction-detail', kwargs={'pk': 1}),
            updated_attraction,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert that the PUT returns the expected 204 status
        self.assertEqual(response.status_code, 204)

        # Get the attraction again, it should now be the updated attraction.
        response = self.client.get(
            reverse('attraction-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert that the name has been updated
        self.assertEqual(response.data["name"], updated_attraction["name"])


if __name__ == '__main__':
    unittest.main()