from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message
from .ai_helper import AIChatBot
import json
from django.template import loader

chatbot = AIChatBot()

def chat_page(request):
    return render(request, r"chat.html")

@csrf_exempt
def chat_endpoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            
            # Create or get conversation
            conversation = Conversation.objects.create(user=request.user if request.user.is_authenticated else None)
            
            # Save user message
            Message.objects.create(
                conversation=conversation,
                content=user_message,
                is_bot=False
            )
            
            # Get conversation history
            history = Message.objects.filter(conversation=conversation).order_by('timestamp')[:5]
            
            # Get bot response
            bot_response = chatbot.get_response(user_message, history)
            
            # Save bot response
            Message.objects.create(
                conversation=conversation,
                content=bot_response,
                is_bot=True
            )
            
            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
