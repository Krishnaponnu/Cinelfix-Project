from django.db import models

# Create your models here.

import uuid

from multiselectfield import MultiSelectField

from embed_video.fields import EmbedVideoField

# Create your models here.

class BaseClass(models.Model):

    uuid=models.UUIDField(unique=True,default=uuid.uuid4)

    active_status=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    class Meta:

        abstract=True

class IndustryChoices(models.TextChoices):

    MOLLYWOOD='Mollywood','Mollywood'

    HOLLYWOOD='Hollywood','Hollywood'

    BOLLYWOOD='Bollywood','Bollywood'

    TOLLYWOOD='Tollywood','Tollywood'

class CertificationChoices(models.TextChoices):

    A='A','A'

    UA='U/A','U/A'

    U='U','U'

    S='S','S'

class GenreChoices(models.TextChoices):

    ACTION = 'Action','Action'

    ROMANTIC = 'Romantic','Romantic'

    THRILLER = 'Thriller','Thriller'

    COMEDY = 'Comedy','Comedy'

    HORROR = 'Horror','Horror'

class ArtistChoices(models.TextChoices):

    MOHANLAL = 'Mohan Lal','Mohan Lal'

    MAMMOOTTY = 'Mammootty','Mammootty'

    NIVINPAULY = 'Nivin Pauly','Nivin Pauly'

class LanguagesChoices(models.TextChoices):

    MALAYALAM = 'Malayalam','Malayalam'

    ENGLISH = 'English','English'

    HINDI = 'Hindi','Hindi'

    TAMIL = 'Tamil','Tamil'

    TELUGU = 'Telugu','Telugu'

    KANNADA = 'Kannada','Kannada'

class Industry(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:
         
        verbose_name = 'Industries'

        verbose_name_plural = 'Industries'
         
    def __str__(self):
         
        return f'{self.name}'
    
class Genre(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:
         
        verbose_name = 'Genre'

        verbose_name_plural = 'Genre'
         
    def __str__(self):
         
        return f'{self.name}'
    
class Artist(BaseClass):

    name = models.CharField(max_length=50)

    dob = models.DateField()

    description = models.TextField()

    class Meta:
         
        verbose_name = 'Artists'

        verbose_name_plural = 'Artists'
         
    def __str__(self):
         
        return f'{self.name}'
    
class Languages(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:
         
        verbose_name = 'Languages'

        verbose_name_plural = 'Languages'
         
    def __str__(self):
         
        return f'{self.name}'


class Movie(BaseClass):
    
    name=models.CharField(max_length=50)

    photo = models.ImageField(upload_to='movies/banner-images')

    #  thumbnail = models.ImageField(upload_to='movies/thumbnails')

    description = models.TextField()

    release_date=models.DateField()

    industry=models.ForeignKey('Industry',on_delete=models.CASCADE)    

    runtime=models.TimeField()

    certification=models.CharField(choices=CertificationChoices.choices)  

    genre=models.ManyToManyField('Genre')

    artist = models.ManyToManyField('Artist')

    video = EmbedVideoField()

    tags = models.TextField()

    languages = models.ManyToManyField('Languages')

    #languages = MultiSelectField(choices=LanguagesChoices.choices)
     
    class Meta:
        
        verbose_name = 'Movies'

        verbose_name_plural = 'Movies'
         
    def __str__(self):
         
        return f'{self.name}'