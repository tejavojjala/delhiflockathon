from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json,logging,requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from pinnedmessages.models import Messages,Reactions,Users
from flock.settings import APP_SECRET,APP_ID,BOT_ID,BOT_TOKEN
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import urllib3,requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['POST'])
def events(request, format = None):

#	urllib3.disable_warnings()	
	if(request.method == 'POST'):
		event_token = request.META["HTTP_X_FLOCK_EVENT_TOKEN"]
		try:
			verify_event_token(event_token = event_token, app_secret = APP_SECRET)
		except:
			return Response(request.data,status=400)
		content = json.loads(JSONRenderer().render(request.data))
		if(content["name"]=="app.install"):
			user = Users.objects.create_user(userId = content["userId"],userToken = content["token"])
			return Response(request.data,status=200)

		elif(content["name"]=="client.messageAction"):
			flock_user = content["userId"]
			flock_user_name = content["userName"]
			groupId = content["chat"]
			isPinned = True
			messageUid = content["messageUids"][0]
			print content
			if(len(Messages.objects.filter(messageUid = messageUid))!=0):
				return Response(request.data,status=400)
			flock_user_token = Users.objects.get(userId = flock_user).userToken
			flock_client = FlockClient(token=flock_user_token, app_id = flock_user)
			userDp = flock_client.get_user_info()["profileImage"]
			msg_details = requests.get("https://api.flock.co/v1/chat.fetchMessages", params={"token": flock_user_token, "uids": "["+messageUid+"]", "chat": groupId})
			text = json.loads(msg_details.text)[0]["text"]
			message = Messages.objects.create_message(flock_user=flock_user, flock_user_name = flock_user_name, userDp = userDp, groupId = groupId, isPinned = isPinned, text = text, messageUid = messageUid)
			message.save()
			return Response(request.data, status = 200)

	return Response(request.data, status = 400)

@xframe_options_exempt
def pinnedmessages(request):
	content = json.loads(request.GET.get("flockEvent"))
	groupId = content["chat"]#"g:115645_lobby"  
	userId =  content["userId"] #"u:ir6xq0ttx00bq66t"
	all_pinned = Messages.objects.filter(groupId = groupId)
	return render(request,'feeds/feeds.html',{'all_pinned':all_pinned, 'userId':userId })

@csrf_exempt
def like(request):
    feed_id = request.POST['feed']
    user_id = request.POST['userId']
    reactionType = "like"
    message = Messages.objects.get(primaryKey=feed_id)
    reactor = Reactions.objects.filter(foreignKey = message, reactorId = user_id)
    if(len(reactor)==0):
    	print "hii"
    	Reactions.objects.create_reaction(message, user_id, reactionType)
    else:
    	print "hii2"
    	reaction = Reactions.objects.get(foreignKey = message, reactorId = user_id)
    	reaction.reactionType = reactionType
    	reaction.save()
    message = Messages.objects.get(primaryKey=feed_id)
    likes = Reactions.objects.filter(foreignKey = message, reactionType = "like")
    print len(likes)
    message.likes = len(likes)
    dislikes = Reactions.objects.filter(foreignKey = message, reactionType = "dislike")
    message.dislikes = len(dislikes)
    message.save()
    return JsonResponse({"likes":message.likes, "dislikes":message.dislikes})

@csrf_exempt
def dislike(request):
    feed_id = request.POST['feed']
    user_id = request.POST['userId']
    reactionType = "dislike"
    message = Messages.objects.get(primaryKey=feed_id)
    reactor = Reactions.objects.filter(foreignKey = message, reactorId = user_id)
    if(len(reactor)==0):
    	print "hii"
    	Reactions.objects.create_reaction(message, user_id, reactionType)
    else:
    	print "hii2"
    	reaction = Reactions.objects.get(foreignKey = message, reactorId = user_id)
    	reaction.reactionType = reactionType
    	reaction.save()
    message = Messages.objects.get(primaryKey=feed_id)
    likes = Reactions.objects.filter(foreignKey = message, reactionType = "like")
    print len(likes)
    message.likes = len(likes)
    dislikes = Reactions.objects.filter(foreignKey = message, reactionType = "dislike")
    message.dislikes = len(dislikes)
    message.save()
    return JsonResponse({"likes":message.likes, "dislikes":message.dislikes})

@csrf_exempt
def remove(request):
    feed_id = request.POST['feed']
    message = Messages.objects.get(primaryKey=feed_id)
    message.delete()
    return HttpResponse(request,status=200)
