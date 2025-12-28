import random

import string

from twilio.rest import Client

from decouple import config

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from movies.models import Movie

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer

def generate_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))

    return password

def generate_otp():

    otp = ''.join(random.choices(string.digits,k=4))

    return otp

def send_otp(phone_num,otp):

    
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_=config('TWILIO_NUM'),
    to=config('MY_NUMBER'),
    body= f'OTP For Verification : {otp}'
    )


def send_email(recipient,template,subject,context):

    sender = config('EMAIL_HOST_USER')

    content = render_to_string(template,context)

    msg = EmailMultiAlternatives(from_email=sender,to=[recipient],subject=subject)

    msg.attach_alternative(content,'text/html')

    msg.send()


def get_recommended_movies(movie):

    data = pd.DataFrame(Movie.objects.all().values('id','name', 'description','industry__name','certification','genre__name','artist__name','tags'))



    data['all_fields'] = data['description']+' '+data['industry__name']+' '+data['certification']+' '+data['genre__name']+' '+data['artist__name']+' '+data['tags']
    
    data.drop(columns=['description','industry__name','certification','genre__name','artist__name','tags'],inplace=True)


    tfidf_vectorizer = TfidfVectorizer(max_features=200, stop_words='english')

    vector = tfidf_vectorizer.fit_transform(data['all_fields']).toarray()

    name = movie.name
    
    similiarity=cosine_similarity(vector)

    my_movie_id=data[data['name']==name].index[0]

    distance=sorted(list(enumerate(similiarity[my_movie_id])),reverse=True,key=lambda vector:vector[1])

    recommended_movies_ids=[]

    for i in distance[0:10]:

        similarity_score = i[1]

        ids = data.iloc[i[0]].id

        if similarity_score > 0.1 and ids!=movie.id:

            recommended_movies_ids.append(ids)

    recommended_movies = Movie.objects.filter(id__in=recommended_movies_ids)

    return recommended_movies