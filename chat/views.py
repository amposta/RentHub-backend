from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, Message
from marketplace.models import RentalItem


@login_required(login_url='accounts:login')
def conversations_list(request):
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('participants').order_by('-updated_at')
    # attach the other participant and a display name to avoid method calls in templates
    conversations = list(conversations)
    for conv in conversations:
        other = conv.get_other_participant(request.user)
        if other:
            display = other.first_name if getattr(other, 'first_name', '') else getattr(other, 'email', '')
        else:
            display = 'Unknown'
        conv.other_display = display

    return render(request, 'chat/conversations.html', {
        'conversations': conversations,
        'page_title': 'Messages',
    })


@login_required
def start_conversation(request, item_id):
    item = get_object_or_404(RentalItem, id=item_id)
    if item.owner == request.user:
        messages.error(request, 'You cannot message yourself about your own listing.')
        return redirect('marketplace:listing_detail', item_id=item.id)

    conversation = Conversation.objects.filter(item=item, participants=request.user).filter(participants=item.owner).first()
    if not conversation:
        conversation = Conversation.objects.create(item=item)
        conversation.participants.add(request.user, item.owner)

    return redirect('chat:conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
            messages.success(request, 'Message sent.')
            return redirect('chat:conversation_detail', conversation_id=conversation.id)
        messages.error(request, 'Message cannot be empty.')

    other_user = conversation.participants.exclude(id=request.user.id).first()
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': conversation.messages.all(),
        'other_user': other_user,
        'page_title': 'Chat',
    })
