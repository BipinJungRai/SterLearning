from django.test import TestCase
from .models import User, Decoration
from pathlib import Path
from django.core.files.images import ImageFile

#Sample data located om sample_data folder
#Includes a placeholder image
ROOT_DIR = Path('sample_data')
image_path = 'Placeholder image.png'

class DecorationTests(TestCase):
    @classmethod
    #Create a valid Decoration
    def setUpTestData(cls):
        d1 = Decoration(name='TestDecoration1',
                        image=ImageFile(open(ROOT_DIR / image_path, 'rb'),
                                        name=image_path))
        d1.save()
        d1.full_clean()
    #Test database records creation of new Decoration
    def test_save_decoration(self):
        db_count = Decoration.objects.all().count()
        decoration = Decoration(name='NewDecoration',
                                image=ImageFile(open(ROOT_DIR / image_path, 'rb'),
                                        name=image_path))
        decoration.save()
        decoration.full_clean()
        self.assertEqual(db_count+1, Decoration.objects.all().count())

class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        u1 = User(username='TestUser1',
                  password='TestPassword1',
                  email='testuser1@test.com')
        u1.save()
        u1.full_clean()
    #Test that a user can be saved with an avatar
    #and inventory avatar filled
    def test_avatar_user(self):
        db_count = User.objects.all().count()
        user = User(username='NewUser',
                    password='NewPassword',
                    email='newuser@test.com',
                    avatar='DK',
                    inventoryAvatar=['TL', 'DK'])
        user.save()
        user.full_clean()
        self.assertEqual(db_count+1, User.objects.all().count())
    #Test that a decoration can be saved to
    #a user and added to inventory
    def test_decoration_user(self):
        d1 = Decoration(name='NewDecoration',
                        image=ImageFile(open(ROOT_DIR / image_path, 'rb'),
                                        name=image_path))
        d1.save()
        d1.full_clean()
        user = User(username='NewUser',
                    password='NewPassword',
                    email='newuser@test.com',
                    avatar='DK',
                    inventoryAvatar=['TL', 'DK'],
                    decoration=d1)
        user.save()
        user.full_clean()
        user.inventoryDecoration.add(d1)
        self.assertEqual(user.inventoryDecoration.all().count(),
                         1)





        
    