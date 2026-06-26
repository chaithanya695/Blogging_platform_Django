from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# creating a class for post 

# posts category section
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cover_image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    second_image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    # here we are connecting this author id with multiple tables,One-to-Many Relationship: we are using foreign key here
    # CASCADE means: If the parent record is deleted, all related child records are automatically deleted.(one user--> many posts)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    likes = models.ManyToManyField(
    User,
    related_name='liked_posts',
    blank=True
    )

    # In Django, auto_now_add=True is used to automatically store the date/time when a record is created.
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at'] #latest posts first

    # The __str__() method defines how an object is displayed as a string.
    def __str__(self):
        return self.title or "Untitled Post"


# each comment belongs to a post
# if post is deleted → comments auto-delete
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:30]}"
    

