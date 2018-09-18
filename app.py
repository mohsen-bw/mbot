from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('mVBiJ+I7W4X9IbfxaAEai62BYY5Mfl7R/AKgpN0DVGrIqXFVHrksQCetTVwegNUPOxDYldg1cyc+rWtjU+34p+fDxEN6dFiW/gq6OSGj+6vOe0YkjtWvzMl2kEILyUCAKFbTx8vyENdoXN13DFJM6AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a606f2ca66d60af4f08830d8bee13b6c')
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
#=====[ TEMPLATE MESSAGE ]=============
    elif text == '/template':
        buttons_template = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                title='[ TEMPLATE MSG ]',
                text= 'Tap the Button',
                actions=[
                    MessageTemplateAction(
                        label='Culum 1',
                        text='/mosen.bw'
                    ),
                    MessageTemplateAction(
                        label='CULUM 2',
                        text='/mosen.bw'
                    ),
                    MessageTemplateAction(
                        label='CULUM 3',
                        text='/mosen.bw'
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, buttons_template)
        {  
  "type": "flex",
  "altText": "this is a flex message",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "hello"
        },
        {
          "type": "text",
          "text": "world"
        }
      ]
    }
  }
}
  {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Header text"
      }
    ]
  },
  "hero": {
    "type": "image",
    "url": "https://example.com/flex/images/image.jpg",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Body text",
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Footer text",
      }
    ]
  },
  "styles": {
    "comment": "See the example of a bubble style object"
  }
}      
#=====[ CAROUSEL MESSAGE ]==========
    elif text == '/carousel':
        message = TemplateSendMessage(
            alt_text='OTHER MENU',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='ADD ME',
                        text='Contact mosen.bw',
                        actions=[
                            URITemplateAction(
                                label='>TAP HERE<',
                                uri='https://line.me/ti/p/~masih.00'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='Instagram',
                        text='FIND ME ON INSTAGRAM',
                        actions=[
                            URITemplateAction(
                                label='>TAP HERE!<',
                                uri='http://line.me/ti/p/~masih.00'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
#=====[ FLEX MESSAGE ]==========
    elif text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://lh5.googleusercontent.com/VoOmR6tVRwKEow0HySsJ_UdrQrqrpwUwSzQnGa0yBeqSex-4Osar2w-JohT6yPu4Vl4qchND78aU2c5a5Bhl=w1366-h641-rw',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://line.me/ti/p/~masih.00', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='mosen.bw', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Tangerang, Iran',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='mosen.bw', uri="https://line.me/ti/p/~masih.00")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
