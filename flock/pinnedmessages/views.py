from django.shortcuts import render
from django.http import HttpResponse
import json,logging,requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from pinnedmessages.models import Messages
from flock.settings import APP_SECRET,APP_ID,BOT_ID,BOT_TOKEN
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import urllib3
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
			return Response(request.data,status=200)
		elif(content["name"]=="client.slashCommand" and content["command"]=="pin"):
			text = content["text"]
			flock_user = content["userId"]
			flock_user_name = content["userName"]
			groupId = content["chat"]
			isPinned = True

			message = Messages.objects.create_message(flock_user=flock_user, flock_user_name = flock_user_name, groupId = groupId, isPinned = isPinned, text = text)
			message.save()

			flock_client = FlockClient(token=BOT_TOKEN, app_id = flock_user)
			print flock_client.get_user_info()


			flock_client = FlockClient(token=BOT_TOKEN, app_id=APP_ID)
#			send_as = SendAs(name=flock_user_name, profile_image='https://pbs.twimg.com/profile_images/1788506913/HAL-MC2_400x400.png')
			send_as_message = Message(to=flock_user, text=text	)
			res = flock_client.send_chat(send_as_message)
			print(res)
			return Response(request.data, status = 200)

	return Response(request.data, status = 400)

@xframe_options_exempt
def pinnedmessages(request):
#	content = json.loads(request.GET.get("flockEvent"))
	groupId = "g:115645_lobby" #content["chat"] 
	userId = "u:ir6xq0ttx00bq66t"  #content["userId"]
	all_pinned = Messages.objects.filter(groupId = groupId)
	return render(request,'feeds/feeds.html',{'all_pinned':all_pinned, 'userId':userId })

@csrf_exempt
def like(request):
    feed_id = request.POST['feed']
    user_id = request.POST['userId']
    print "hii"
    message = Messages.objects.get(primaryKey=feed_id)
    message.likes = message.likes + 1
    message.save()
    return HttpResponse(message.likes)

@csrf_exempt
def dislike(request):
    feed_id = request.POST['feed']
    user_id = request.POST['userId']
    message = Messages.objects.get(primaryKey=feed_id)
    message.dislikes = message.dislikes + 1
    message.save()
    return HttpResponse(message.dislikes)
