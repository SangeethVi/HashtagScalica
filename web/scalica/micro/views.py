from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm , SubscribeForm, Topic, Subscription

import six

import RAKE.RAKE as rake
import operator
import io

stoppath = "/home/sangeethvishnu/depot/web/scalica/micro/SmartStoplist.txt"

rake_object = rake.Rake(stoppath,1, 1, 1)

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):  
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1) 
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()
    text=new_post.text
    sentenceList = rake.split_sentences(text)

    for sentence in sentenceList:
      print("Sentence:", sentence)

    # generate candidate keywords
    stopwords = rake.load_stop_words(stoppath)
    stopwordpattern = rake.build_stop_word_regex(stoppath)
    phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern, stopwords)
    print("Phrases:", phraseList)

    # calculate individual word scores
    wordscores = rake.calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
    for candidate in keywordcandidates.keys():
      print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))

    # sort candidates by score to determine top-scoring keywords
    sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
    
    for keywords in sortedKeywords:
    	print("Keyword: " +str(keywords) +"\n")

    print(rake_object.run(text))
    x=rake_object.run(text)
  
    if len(x)==0:
        x = sortedKeywords[0][0]
    else:
	      x = x[0][0]
    # if topic is already in topics table, just add to posts object
    if len(Topic.objects.filter(topic = x)) > 0:
      topics = Topic.objects.get(topic = x)
      topics.posts.add(new_post)
    # if topic is not in topics table, create it and add the new post
    else: 
      newTopic = Topic(topic = x)
      newTopic.save()
      newTopic.posts.add(new_post)

    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})


@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.follower = request.user
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})

#allows you to subscribe to a topic
@login_required
def subscribe(request):
  if request.method == 'POST':
    form = SubscribeForm(request.POST)
    new_sub = form.save(commit=False)
    new_sub.user = request.user
    new_sub.save()
    return home(request)
  else:
    form = SubscribeForm
  return render(request, 'micro/subscribe.html', {'form': form})

#allows you to search for a topic
@login_required
def search(request):
  if request.method == 'POST':
    
    print(request.POST['search1'])
    found = Topic.objects.filter(topic=request.POST['search1'])
    print(found)
    return render(request, 'micro/search.html', {'found': found})
  
