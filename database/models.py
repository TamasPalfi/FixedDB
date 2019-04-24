from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime


# Create your models here.
class Member(models.Model):

    invited_by   = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    visibility  = models.BooleanField(default=False, null=True)
    email       = models.CharField(max_length=50,null=True)
    password    = models.CharField(max_length=50,null=True)
    first_name    = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    points      = models.IntegerField(null=True)
    user_type   = models.CharField(max_length=50,null=True)
    date_created = models.DateTimeField(auto_now_add = True,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    birthday    = models.CharField(max_length=50,null=True)
    address     = models.CharField(max_length=50,null=True)

    def create_member(self, invited_by, email, password, first_name, last_name, birthday, address, points=0):
        """
        Creates a new object with the given arguments, saving it to the database
        and returning the created object.
        """
        member = Member.objects.create(visibility=True, points=0, is_verified=False, invited_by=invited_by, email=email,
                                       password=password, first_name=first_name, last_name=last_name, user_type=Member,
                                       date_created=datetime.datetime.now(), birthday=birthday, address=address)
        member.save(force_insert=True, using=self.db)  # force_insert may need to be false
        return member

    def data(self):
        return self.__dict__

    # def get_member(self, email):
    #     member = Member.objects.order_by(email).first()
    #     return member
        
    def set_visibility(self, visibility):
        self.visibility = visibility

    def set_email(self, email):
        self.email = email
    
    def set_password(self, password):
        self.password = password

    def set_username(self, username):
        self.username = username
    
    def set_points(self, points):
        self.points = points

    def set_user_type(self, user_type):
        self.user_type = user_type
    
    def set_is_verified(self, is_verified):
        self.is_verified = is_verified
    
    def set_username(self, username):
        self.username = username
    
    def set_birthday(self, birthday):
        self.birthday = birthday
    
    def set_address(self, address):
        self.address = address

    def remove_member(self):
        # Not sure how to check if the deletion occurred correctly...
        self.delete(keep_parents=True)


class Post(models.Model):
    user            = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    urls            = models.CharField(max_length=100, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_modified   = models.DateTimeField(auto_now=True, null=True)
    is_flagged      = models.BooleanField(default=False, null=True)
    content         = models.TextField(max_length=1000000, null=True)
    by_admin        = models.BooleanField(default=False, null=True)

    def create_post(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self.for_write = True
        obj.save(force_insert=True, using=self.db) # force_insert may need to be false
        return obj

    def data(self):
        return self.__dict__

    def set_urls(self, urls):
        self.urls = urls
    
    def set_is_flagged(self, is_flagged):
        self.is_flagged = is_flagged
    
    def set_content(self, content):
        self.content = content
    
    def set_by_admin(self, by_admin):
        self.by_admin = by_admin

    def remove_post(self):
        # Not sure how to check if the deletion occurred correctly...
        self.delete(keep_parents=True)


class Comment(models.Model):
    replies         = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    post            = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user            = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    content         = models.TextField(max_length=1000000, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_modified   = models.DateTimeField(auto_now=True, null=True)
    by_admin        = models.BooleanField(default=False, null=True)

    def create_comment(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self.for_write = True
        obj.save(force_insert=True, using=self.db) # force_insert may need to be false
        return obj

    def get_comment(self):
        return self

    def set_content(self, content):
        self.content = content

    def set_by_admin(self, by_admin):
        self.by_admin = by_admin

    def remove_comment(self):
        # Not sure how to check if the deletion occurred correctly...
        self.delete(keep_parents=True)


class CreditCard(models.Model):
    user            = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    card_num        = models.CharField(max_length=16, null=True)
    cvv             = models.CharField(max_length=3, null=True)
    holder_name     = models.CharField(max_length=50, null=True)
    card_expiration = models.CharField(max_length=25, null=True)
    currently_used  = models.BooleanField(default=True, null=True)
    address         = models.CharField(max_length=50,null=True)
    zipcode         = models.IntegerField(null=True)

    def create_cc(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self.for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def get_cc(self):
        return self
        
    def set_content(self, card_num):
        self.card_num = card_num

    def set_content(self, cvv):
        self.cvv = cvv

    def set_content(self, holder_name):
        self.holder_name = holder_name

    def set_content(self, card_expiration):
        self.card_expiration = card_expiration

    def set_content(self, currently_used):
        self.currently_used = currently_used

    def set_content(self, address):
        self.address = address

    def set_content(self, zipcode):
        self.zipcode = zipcode

    def remove_cc(self):
        self.delete(keep_parents=True)


class Image(models.Model):
    user                = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    post                = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image_original      = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    filter_used         = models.BooleanField(default=False, null=True)
    current_image       = models.ImageField(null=True)
    is_flagged          = models.BooleanField(default=False, null=True)
    by_admin            = models.BooleanField(default=False, null=True)

    def create_image(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self.for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def data(self):
        return self.__dict__

    def set_is_flagged(self, is_flagged):
        self.is_flagged = is_flagged

    def set_by_admin(self, by_admin):
        self.by_admin = by_admin

    def remove_image(self):
        self.delete(keep_parents=True)


class Filter(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    filter_name = models.CharField(max_length=16, null=True)

    def create_filter(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self.for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def data(self):
        return self.__dict__
    
    def set_filter_name(self, filter_name):
        self.filter_name = filter_name

    def remove_filter(self):
        self.delete(keep_parents=True)

