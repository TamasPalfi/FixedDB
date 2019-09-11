from django.test import TestCase
from database.models import Member, Post, Comment, CreditCard, Image, Filter
import tempfile
import unittest


class MemberTestCase(TestCase): 

    # Test creating an member object
    def create_member(self, name, invitedby=None):
        return Member.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")

    def test_create(self):
        new_member = self.create_member("new-user")
        self.assertTrue(isinstance(new_member, Member))
        # since we created a new member, the number should increase to 1
        self.assertEqual(Member.objects.count(), 1)

    def test_class_create(self):
        new_member = Member.create_memb(invited_by='Owen', email='owenc@gmail.com', password='1234',
                                          first_name='Owen', last_name='Carpenter', birthday='10/05/1997',
                                          address='UMass')
        self.assertTrue(isinstance(new_member, Member))
        self.assertEqual(Member.objects.count(), 2)   # Is the other get method actually saving to the database?

    # Get the object
    def test_get_specific_data(self):
        new_member = self.create_member("new-user")
        # # get the username
        username = new_member.data()['username']
        # make sure I get the expected value 
        self.assertEqual("new-user", username)

    # Get the object by id
    def test_get_byid(self):
        new_member = self.create_member("new-user")
        # get id
        new_member_id = new_member.data()['id']
        # get member model by the id
        username = Member.objects.get(id=new_member_id).data()['username']
        # make sure I get the expected value 
        self.assertEqual("new-user", username)
    
    # Edit the object
    def test_edit(self):
        new_member = self.create_member("new-user")
        # update the value
        new_member.set_username("new-user")
        # get new username
        new_name = new_member.data()['username']
        self.assertEqual("new-user", new_name)

    def test_set_points(self):
        new_member = Member.create_member(invited_by='Owen', email='owenc@gmail.com', password='1234',
                                          first_name='Owen', last_name='Carpenter', birthday='10/05/1997',
                                          address='UMass')

        new_member = new_member.set_points(1)

        self.assertEqual(new_member.data().points, 1)

    # Delete the object
    def test_delete(self):
        new_member = self.create_member("new-user")

        # make sure the new object exists
        self.assertEqual(Member.objects.count(),1)
        
        # delete the object by id
        id = new_member.data()['id']
        Member.objects.filter(id=id).delete()
        
        # since we delete the object, there should be no member in the table.
        self.assertEqual(Member.objects.count(), 0)

    def test_remove_method(self):
        new_member = Member.create_member(invited_by='Owen', email='owenc@gmail.com', password='1234',
                                          first_name='Owen', last_name='Carpenter', birthday='10/05/1997',
                                          address='UMass')
        new_member.remove_member()

        self.assertEqual(Member.objects.count(), 0)
    
    # Test Invite by 
    def test_inviteby(self):
        idol = self.create_member('idol')
        member = self.create_member('member', idol)

        # check who invited member
        invitedby_id = member.data()['invitedby_id']
        who_invited_member = Member.objects.get(id=invitedby_id).data()['username']

        # Idol Invited Member
        self.assertEqual("idol", who_invited_member)


class PostTestCase(TestCase): 

    def create_member(self, name, invitedby=None):
        return Member.objects.create(visibility=True,
                                    invited_by= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")

    def create_post(self, content, user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)

    # Test creating an Post object
    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        self.assertTrue(isinstance(new_post, Post))
        # since we created a new post, the number should increase to 1
        self.assertEqual(Post.objects.count(),1)
    
    # Who wrote this post?
    def test_writer(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        writer_id = new_post.data()['user_id']
        writer_name = Member.objects.get(id=writer_id).data()['username']
        self.assertEqual("new-user",writer_name)
       
    #Rob wrote this, test to see if the functions in Models.py work
    def test_set_urls(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        new_post.set_urls("www.cooltest.com")
        url = new_post.data()['urls']
        self.assertEqual("www.cooltest.com",url)
    


class CommentTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user = user,
                                   urls    = "www.test.com",
                                   is_flagged = False,
                                   content = content,
                                   by_admin = False)
    
    def create_comment(self,content,user,post,replies=None):
        return Comment.objects.create(user = user,
                                      post = post,
                                      replies = replies,
                                      content = content,
                                      by_admin = False)
                                      
    def test_create(self):
        new_member = self.create_member("new-user")
        coment_user = self.create_member("comment-user")
        new_post = self.create_post("hello",new_member)
        new_comment = self.create_comment("this is a comment",coment_user,new_post)
        self.assertTrue(isinstance(new_comment, Comment))
        # since we created a new post, the number should increase to 1
        self.assertEqual(Comment.objects.count(),1)
    
    # Check linked Post
    def test_create(self):
        new_member = self.create_member("new-user")
        coment_user = self.create_member("comment-user")
        new_post = self.create_post("hello",new_member)
        new_comment = self.create_comment("this is a comment",coment_user,new_post)
        
        post_id = new_comment.data()['post_id']
        post_content = Post.objects.get(id=post_id).data()['content']

        self.assertEqual("hello",post_content)


class CreditCardTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_card(self,user):
        return CreditCard.objects.create(user=user,
                                         card_num="0000111122223333",
                                         cvv="123",
                                         holder_name="test-user",
                                         card_expiration="20201012",
                                         currently_used=True,
                                         address="earth",
                                         zipcode=10001)
    def test_create(self):
        new_member = self.create_member("new-user")
        new_card = self.create_card(new_member)
        self.assertTrue(isinstance(new_card, CreditCard))
        # since we created a new post, the number should increase to 1
        self.assertEqual(CreditCard.objects.count(),1)
                                

class ImageTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
                                    invitedby=invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user=user,
                                   urls="www.test.com",
                                   is_flagged=False,
                                   content=content,
                                   by_admin=False)

    def create_image(self,user,post,image):
        return Image.objects.create(user=user,
                                    post=post,
                                    current_image=image,
                                    is_flagged=False,
                                    by_admin=False )
    
    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello", new_member)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        new_image = self.create_image(new_member,new_post, image)
        self.assertTrue(isinstance(new_image, Image))
        self.assertEqual(Image.objects.count(), 1)
        
    def test_class_create(self):
        new_member = Member.create_memb(invited_by='Tamas', email='tamasp@gmail.com', password='4821',
                                          first_name='Bobby', last_name='Builder', birthday='10/03/1929',
                                          address='Nova Scotia')
        new_post = self.create_post("hello???", new_member)
        new_image = self.create_image(new_member,new_post, image)
        self.assertTrue(isinstance(new_image, Image))
        self.assertEqual(Image.objects.count(), 2) 
     
    def test_get_specific_data(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello", new_member)
        new_image = self.create_image(new_member,new_post, imageID)
        # get the originial_image_id
        orig_img_id = new_image.data()['original_image_id']
        # test that the image ID matches
        self.assertEqual("imageID", orig_img_id)
        
    def test_set(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello", new_member)
        new_image = self.create_image(new_member,new_post, imageID)
        # set new orginal_image_id
        new_image.set_orginal_image_id(3036)
        # get the new id
        new_id = new_image.data()['original_image_id]
        self.assertEqual(3036, new_id) 
                                  
    def test_delete(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello", new_member)
        new_image = self.create_image(new_member,new_post, imageID)
        # assert statement to make sure new image is in database
        self.assertEqual(Image.objects.count(),1)
        # delete image by ID
        id = new_image.data()['original_image_id']
        Image.objects.filter(original_image_id=id).delete()
        # assert statement to check that image was deleted (not in database)
        self.assertEqual(Image.objects.count(), 0)

        
class FilterTestCase(TestCase): 

    def create_member(self,name,invitedby=None):
        return Member.objects.create(visibility=True,
                                    invitedby= invitedby,
                                    email="email@email.com",
                                    password="pwd",
                                    username=name,
                                    points="10",
                                    user_type="Member",
                                    is_verified=True,
                                    birthday="19980903",
                                    address="earth")
    
    def create_post(self,content,user=None):
        return Post.objects.create(user=user,
                                   urls="www.test.com",
                                   is_flagged=False,
                                   content=content,
                                   by_admin=False)

    def create_image(self,user,post,image):
        return Image.objects.create(user=user,
                                    post=post,
                                    current_image=image,
                                    is_flagged=False,
                                    by_admin=False)
    
    def create_filter(self,image):
        return Filter.objects.create(image=image, filter_name="test-filter")

    def test_create(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello",new_member)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        new_image = self.create_image(new_member,new_post, image)
        new_filter = self.create_filter(new_image, filter_id)

        self.assertTrue(isinstance(new_filter, Filter))
        self.assertEqual(Filter.objects.count(), 1)
                                  
    def test_set(self):
        new_member = self.create_member("new-user")
        new_post = self.create_post("hello", new_member)
        new_image = self.create_image(new_member,new_post, imageID)
        new_filter = self.create_filter(new_image, filter_id)
        # set new filter_id
        new_filter.set_filter_id(2121)
        # get the new id
        new_id = new_filter.data()['filter_id]
        self.assertEqual(2121, new_id) 
