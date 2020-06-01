from django.test import TestCase
from django.urls import reverse
from kennywoodapi.models import Itinerary, Customer, Attraction, ParkArea
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import unittest


class TestItineraries(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        self.username = 'TestUser'
        self.password = 'Test123'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, family_members=9)

    def testPostItinerary(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )
      
        # Create an itinerary
        new_itinerary = {
            "attraction_id": 1,
            "customer_id": 1,
            "starttime": 1
        }

        # Use the client to make the HTTP POST request and store the response
        response = self.client.post(
            reverse('itinerary-list'), new_itinerary, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert: Does the status code of the HTTP response indicate that the it was successful?
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one itinerary instance in there. Since we are testing a POST request, we use the ORM to make sure the item was created in the database. Remember, the tests are run against a testing database that initially has no data.
        # Assert: Is there one new itinerary in the database?
        self.assertEqual(Itinerary.objects.count(), 1)

        # Assert: Is the itinerary in the database the one we just created?
        self.assertEqual(Itinerary.objects.get().attraction_id, new_itinerary["attraction_id"])
    
    def testGetitinerary(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )
      
        new_itinerary = Itinerary.objects.create(
            attraction_id=1,
            customer_id=1,
            starttime=1
        )

        response = self.client.get(
            reverse('itinerary-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["attraction_id"], new_itinerary.attraction_id)

        # There are no characters, so this was removed from the process:
        # self.assertIn(new_itinerary.attraction_id.encode(), response.content)
        
    def testDeleteItinerary(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )
      
        new_itinerary = Itinerary.objects.create(
            attraction_id=1,
            customer_id=1,
            starttime=1
        )

        # Delete a itinerary. As shown in our post and get tests above, new_itinerary
        # will be the only itinerary in the database, and will have an id of 1
        response = self.client.delete(
            reverse('itinerary-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 204.
        self.assertEqual(response.status_code, 204)

        # Confirm that the itinerary is NOT in the database, which means there is nothing in the itinerary table.
        response = self.client.get(
            reverse('itinerary-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)
        
    def testEditItinerary(self):
        new_parkarea = ParkArea.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )
      
        new_attraction = Attraction.objects.create(
            name="Test Attraction Area",
            area_id=1
        )
      
        new_itinerary = Itinerary.objects.create(
            attraction_id=1,
            customer_id=1,
            starttime=1
        )

        # Create new updated parkare.
        updated_itinerary = {
            "attraction_id": 1,
            "customer_id": 1,
            "starttime": 5
        }

        # Update the itinerary in the db
        response = self.client.put(
            reverse('itinerary-detail', kwargs={'pk': 1}),
            updated_itinerary,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert that the PUT returns the expected 204 status
        self.assertEqual(response.status_code, 204)

        # Get the itinerary again, it should now be the updated itinerary.
        response = self.client.get(
            reverse('itinerary-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert that the name has been updated
        self.assertEqual(response.data["starttime"], updated_itinerary["starttime"])


if __name__ == '__main__':
    unittest.main()