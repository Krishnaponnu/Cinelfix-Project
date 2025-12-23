from django.shortcuts import render,redirect

from django.views import View

from .models import Movie,IndustryChoices,GenreChoices,ArtistChoices,LanguagesChoices,CertificationChoices

from .forms import MovieForm

from django.db.models import Q

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_user_roles

# Create your views here.

class HomeView(View):

    template = 'home.html'

    def get(self,request,*args,**kwargs):

        data = {'page':'Home'}

        return render(request,self.template,context=data)
    
class MovieListView(View):

    template = 'movies/movie-list.html'

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        movies = Movie.objects.filter(active_status=True)

        if query :

            movies = movies.filter (Q(name__icontains=query)|
                                   Q(description__icontains=query)|
                                   Q(industry__name__icontains=query)|
                                   Q(certification__icontains=query)|
                                   Q(genre__name__icontains=query)|
                                   Q(artist__name__icontains=query)|
                                   Q(languages__name__icontains=query)|
                                   Q(tags__icontains=query)).distinct()

        
                                    

        data = {'page' : 'Movies','movies':movies,'query':query}

        return render(request,self.template,context=data)
    
# class MovieCreateView(View):

#     def get(self,request,*args,**kwargs):

#         industry_choices = IndustryChoices

#         genre_choices = GenreChoices

#         languages_choices = LanguagesChoices

#         artist_choices = ArtistChoices

#         certification_choices = CertificationChoices


#         data = {'page' : 'create Movie',
#                 'industry_choices':industry_choices,
#                 'genre_choices':genre_choices,
#                 'languages_choices':languages_choices,
#                 'artist_choices':artist_choices,
#                 'certification_choices':certification_choices
#                 }

#         return render(request,'movies/movie-create.html',context=data)
    
#     def post(self,request,*args,**kwargs):

#         # print(request.POST)

#         movie_data = request.POST

#         name = movie_data.get('name')

#         photo = request.FILES.get('photo')

#         description = movie_data.get('description')

#         release_date = movie_data.get('release_date')

#         runtime = movie_data.get('runtime')

#         certification = movie_data.get('certification')

#         industry = movie_data.get('industry')

#         languages = movie_data.get('languages')

#         genre = movie_data.get('genre')

#         artist = movie_data.get('artist')

#         video = movie_data.get('video')

#         tags = movie_data.get('tags')

#         Movie.objects.create(name=name,
#                              photo=photo,
#                              description=description,
#                              release_date=release_date,
#                              industry=industry,
#                              runtime = runtime,
#                              certification = certification,
#                              genre = genre,
#                              artist = artist,
#                              video = video,
#                              tags = tags,
#                              languages = languages)

#         #print(name,photo,description,release_date,runtime,certification,industry,languages,genre,artist,video,tags)

#         return redirect('movie-list')

@method_decorator(permitted_user_roles(['Admin']),name='dispatch')
class MovieCreateView(View):

    form_class = MovieForm

    template = 'movies/movie-create.html'

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'page' : 'create Movie',
                'form':form
                }

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return redirect('movie-list')
        
        data = {'form':form,'page':'Create Movie'}
        
        return render(request,self.template,context=data)
    
# class MovieDetailsView(View):

#     template = 'movies/movie-details.html'

#     def get(self,request,*args,**kwargs):

#         return render(request,self.template)
    
class MovieDetailsView(View):

    template = 'movies/movie-details.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        data = {'movie':movie,'page':movie.name}
        
        return render(request,self.template,context=data)
    
@method_decorator(permitted_user_roles(['Admin']),name='dispatch')    
class MovieEditView(View):

    form_class = MovieForm

    template = 'movies/movie-edit.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        form = self.form_class(instance=movie)

        data = {'form':form,'page':movie.name}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        form = self.form_class(request.POST,request.FILES,instance=movie)

        if form.is_valid():

            form.save()

            return redirect('movie-details',uuid=uuid)
        
        data = {'form':form,'page':movie.name}

        return render(request,self.template,context=data)
    
@method_decorator(permitted_user_roles(['Admin']),name='dispatch')    
class MovieDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        #movie.delete()

        movie.active_status = False

        movie.save()
        
        return redirect('movie-list')