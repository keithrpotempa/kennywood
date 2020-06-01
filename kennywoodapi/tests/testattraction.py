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
      
        # Create an itinerary
        new_attraction = {
            "name": "ATTRACTION",
            "area_id": 1
        }

        # Use the client to make the HTTP POST request and store the response
        response = self.client.post(
            reverse('attraction-list'), new_attraction, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert: Does the status code of the HTTP response indicate that the it was successful?
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one attraction instance in there. Since we are testing a POST request, we use the ORM to make sure the item was created in the database. Remember, the tests are run against a testing database that initially has no data.
        # Assert: Is there one new itinerary in the database?
        self.assertEqual(Attraction.objects.count(), 1)

        # Assert: Is the attraction in the database the one we just created?
        self.assertEqual(Attraction.objects.get().name, new_attraction["name"])
    
    @unittest.skip("haven't built yet")
    def testGetitinerary(self):
        new_attraction = itinerary.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )

        # Now we can grab all the itinerarys (meaning the one we just created) from the db
        response = self.client.get(
            reverse('itinerary-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # There's just one product in our testing db, so our collection of itinerarys that we get back as a response should have one itinerary.
        self.assertEqual(len(response.data), 1)
        # Remember, response.data is the Python serialized data used to render the JSON, while response.content is the JSON itself.

        # First, test the contents of the data before serialization
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["name"], new_attraction.name)

        # Then, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_attraction.name.encode(), response.content)
        
    @unittest.skip("haven't built yet")
    def testDeleteitinerary(self):
        new_attraction = itinerary.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )

        # Delete a itinerary. As shown in our post and get tests above, new_attraction
        # will be the only itinerary in the database, and will have an id of 1
        response = self.client.delete(
            reverse('itinerary-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 204.
        self.assertEqual(response.status_code, 204)

        # Confirm that the itinerary is NOT in the database, which means there is nothing in the itinerary table.
        response = self.client.get(
            reverse('itinerary-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)
        
    @unittest.skip("haven't built yet")
    def testEdititinerary(self):
        new_attraction = itinerary.objects.create(
            name="Test Park Area",
            theme="Integration tests"
        )

        # Create new updated parkare.
        updated_itinerary = {
            "name": "Updated Test Park Area",
            "theme": "Integration tests"
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
        self.assertEqual(response.data["name"], updated_itinerary["name"])


if __name__ == '__main__':
    unittest.main()