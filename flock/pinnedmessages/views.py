from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json,logging,requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from pinnedmessages.models import Messages,Reactions,Users,Comments
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
			groupName = content["chatName"]
			isPinned = True
			messageUid = content["messageUids"][0]
			if(len(Messages.objects.filter(messageUid = messageUid))!=0):
				return Response(request.data,status=400)
			flock_user_token = Users.objects.get(userId = flock_user).userToken
			flock_client = FlockClient(token=flock_user_token, app_id = flock_user)
			userDp = flock_client.get_user_info()["profileImage"]
			msg_details = requests.get("https://api.flock.co/v1/chat.fetchMessages", params={"token": flock_user_token, "uids": "["+messageUid+"]", "chat": groupId})
			text = json.loads(msg_details.text)[0]["text"]
			if(flock_user!=json.loads(msg_details.text)[0]["from"]):
				return Response(request.data,status=400)
			message = Messages.objects.create_message(flock_user=flock_user, flock_user_name = flock_user_name, userDp = userDp, groupId = groupId, isPinned = isPinned, text = text, messageUid = messageUid)
			message.save()
			allmembers = flock_client.get_group_members(groupId)
			for i in range(0,len(allmembers)):
				flock_client = FlockClient(token=BOT_TOKEN,app_id=APP_ID)
				user_guid = allmembers[i]["id"]
				simple_message=""
				if(user_guid!=flock_user):
					simple_message = Message(to=user_guid,text=flock_user_name+" pinned a message in group "+groupName)
				else:
					simple_message = Message(to=user_guid,text="You pinned a message in group "+groupName)					
				res = flock_client.send_chat(simple_message)
			return Response(request.data, status = 200)

		elif(content["name"]=="app.uninstall"):
			user = User.objects.get(userId=content["userId"])
			user.delete()
			return Response(request.data,status=200)

	return Response(request.data, status = 400)

@xframe_options_exempt
def pinnedmessages(request):
	content = json.loads(request.GET.get("flockEvent"))
	groupId = content["chat"]#"g:115645_lobby"  
	userId =  content["userId"] #"u:ir6xq0ttx00bq66t"
	all_pinned = Messages.objects.filter(groupId = groupId).order_by('-date')
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
    flock_client = FlockClient(token=BOT_TOKEN,app_id=APP_ID)
    user_guid = message.userId
    groupName = message.groupId
    simple_message = Message(to=user_guid,text="You have "+str(len(likes))+" likes and "+ str(len(dislikes))+"dislikes for a message you pinned in "+groupName)
    res = flock_client.send_chat(simple_message)
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
    flock_client = FlockClient(token=BOT_TOKEN,app_id=APP_ID)
    user_guid = message.userId
    groupName = message.groupId
    simple_message = Message(to=user_guid,text="You have "+str(len(likes))+" likes and "+ str(len(dislikes))+"dislikes for a message you pinned in "+groupName)
    res = flock_client.send_chat(simple_message)
    return JsonResponse({"likes":message.likes, "dislikes":message.dislikes})

@csrf_exempt
def remove(request):
    feed_id = request.POST['feed']
    message = Messages.objects.get(primaryKey=feed_id)
    message.delete()
    return HttpResponse(request,status=200)

@csrf_exempt
def removeComment(request):
    feed_id = request.POST['feed']
    print feed_id
    comment = Comments.objects.get(primaryKey=feed_id)
    message = comment.parent
    comment.delete()
    allComments = Comments.objects.filter(parent = message).order_by('-date')
    return render(request, 'feeds/partial_feed_comments.html',{'allComments': allComments, 'user':userId})

@csrf_exempt
def comment(request):
	if(request.method == 'POST'):
		feed_id = request.POST['feed']
		userId = request.POST['userId']
		flock_user_token = Users.objects.get(userId = userId).userToken
		flock_client = FlockClient(token=flock_user_token, app_id = userId)
		userInfo = flock_client.get_user_info()
		userDp = userInfo["profileImage"]
		post = request.POST['post']
		post = post.strip()
		print "yoobitch"
		if len(post) > 0:
			post = post[:255]
			message = Messages.objects.get(primaryKey = feed_id)
			Comments.objects.create_comment(userId=userId,userName=userInfo["firstName"]+" "+userInfo["lastName"],userDp=userDp,text=post,parent = message)
			allComments = Comments.objects.filter(parent = message).order_by('-date')
			message.numcomments = len(allComments)
			message.save()
			flock_client = FlockClient(token=BOT_TOKEN,app_id=APP_ID)
			user_guid = message.userId
			groupName = message.groupId
			simple_message = Message(to=user_guid,text="You received a new comment for a post you pinned in "+groupName)
			res = flock_client.send_chat(simple_message)
			return render(request, 'feeds/partial_feed_comments.html',{'allComments': allComments, 'user':userId})
	else:
		feed_id = request.GET.get('feed')
		userId = request.GET.get('userId')
		message = Messages.objects.get(primaryKey = feed_id)
		allComments = Comments.objects.filter(parent = message).order_by('-date')
		print allComments
		return render(request, 'feeds/partial_feed_comments.html',{'allComments': allComments, 'user':userId})
	return HttpResponse(status=400)
