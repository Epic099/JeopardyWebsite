import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import time
from . import models

class JeopardyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chess_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        self.send(text_data=json.dumps({
            'type' : "debug",
            'message' : 'Connection to Server established'
        }))
        
        lobby = models.Lobby.objects.filter(Lobby_id=self.room_name).first()
      
        players = lobby.users.all()
        users = []
        for player in players:
            buz = 0 if player != lobby.buzzered_player else 1
            users.append({"name" : player.user.username, "points" : player.Points, "buzzered" : buz})
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
            {
                'type':'update_users',
                'users':users,
                'timer' : 0
            }
        )
    def receive(self, text_data):
        data = json.loads(text_data)
        typ = data['type']
        print(self.room_name)
        lobby = models.Lobby.objects.filter(Lobby_id=self.room_name).first()
        board = lobby.get_board()
        request_user = self.scope["user"]
        if typ == "question":
            if request_user != lobby.host:
                return
            index = data["index"]
            index1 = int(index[:1])-1
            index2 = int(index[-1:])
            q = getattr(board.categories[index1], f"q{index2}")[0]
            category = board.categories[index1].name
            quest = q.question
            a = q.answer
            p = q.points
            lobby.started_time = str(time.time())
            lobby.question = data["index"]
            lobby.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'question',
                    'category':category,
                    'question': quest,
                    'answer': a,
                    'points' : p
                    
                }
            )
        elif typ == "buzzer":
            user = self.scope["user"]
            player = models.Player.objects.filter(user=user).first()
            if lobby.buzzered_player is None:
                lobby.buzzered_player = player
                lobby.buzzered_time = str(time.time())
                lobby.save()
                players = lobby.users.all()
                users = []
                for player in players:
                    buz = 0 if player != lobby.buzzered_player else 1
                    users.append({"name" : player.user.username, "points" : player.Points, "buzzered" : buz})
                d = float(lobby.buzzered_time) - float(lobby.started_time)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'update_users',
                        'users':users,
                        'timer' : 1
                    }
                )
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'debug',
                        'text':f"User {lobby.buzzered_player.user.username} buzzered ({d}s, {d*1000}ms)",
                    }
                )
            else:
                d = time.time() - float(lobby.started_time)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'debug',
                        'text':f"User {lobby.buzzered_player.user.username} tried to buzzer but wasnt first ({d}s, {d*1000}ms)",
                    }
                )
        elif typ == "right":
            if request_user != lobby.host:
                return
            if lobby.buzzered_player is None:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'debug',
                        'text':f"No one buzzered",
                    }
                )
                return
            points = data["points"]
            lobby.buzzered_player.Points += points
            lobby.buzzered_player.save()
            
            index = lobby.question
            
            lobby.buzzered_player = None
            lobby.buzzered_time = ""
            lobby.started_time = ""
            lobby.question = ""
            lobby.save()
            players = lobby.users.all()
            users = []
            for player in players:
                users.append({"name" : player.user.username, "points" : player.Points, "buzzered" : 0})
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'update_users',
                    'users':users,
                    'timer' : 0
                }
            )
            board = lobby.get_board()
            index1 = int(index[:1])-1
            index2 = int(index[-1:])
            board.categories
            
            q = getattr(board.categories[index1], f"q{index2}")[0]
            q.done = True
            
            setattr(board.categories[index1], f"q{index2}", [q])
            lobby.set_board(board)
            lobby.save()
            
            no = []
            
            for i in range(0, len(board.categories)):
                cat = board.categories[i]
                for q in cat.questions:
                    if q.done:
                        no.append(f"{i+1}-{int(q.points/100)}")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'update_board',
                    'exclude' : no,
                }
            )
            
        elif typ == "wrong":
            if request_user != lobby.host:
                return
            if lobby.buzzered_player is None:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'debug',
                        'text':f"No one buzzered",
                    }
                )
                return
            points = data["points"]
            lobby.buzzered_player.Points -= points
            lobby.buzzered_player.save()
            
            
            lobby.buzzered_player = None
            lobby.buzzered_time = ""
            lobby.save()
            players = lobby.users.all()
            users = []
            for player in players:
                users.append({"name" : player.user.username, "points" : player.Points, "buzzered" : 0})
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'update_users',
                    'users':users,
                    'timer' : 0
                }
            )
        elif typ == "skip":
            index = lobby.question
            lobby.buzzered_player = None
            lobby.buzzered_time = ""
            lobby.started_time = ""
            lobby.question = ""
            lobby.save()
            players = lobby.users.all()
            users = []
            for player in players:
                users.append({"name" : player.user.username, "points" : player.Points, "buzzered" : 0})
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'update_users',
                    'users':users,
                    'timer' : 0
                }
            )
            board = lobby.get_board()
            index1 = int(index[:1])-1
            index2 = int(index[-1:])
            board.categories
            
            q = getattr(board.categories[index1], f"q{index2}")[0]
            q.done = True
            
            setattr(board.categories[index1], f"q{index2}", [q])
            lobby.set_board(board)
            lobby.save()
            
            no = []
            
            for i in range(0, len(board.categories)):
                cat = board.categories[i]
                for q in cat.questions:
                    if q.done:
                        no.append(f"{i+1}-{int(q.points/100)}")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'update_board',
                    'exclude' : no,
                }
            )
            
    def debug(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({
            'type':'debug',
            'message': text
        }))
    def question(self, event):
        question = event["question"]
        answer = event["answer"]
        points = event["points"]
        category = event["category"]
        self.send(text_data=json.dumps({
            'type':'question',
            'category': category,
            'question':question,
            'answer': answer,
            'points' : points
        }))
    def update_users(self, event):
        users = event["users"]
        timer = event["timer"]
        self.send(text_data=json.dumps({
            'type':'update_users',
            'users':users,
            'timer' : timer
        }))
    def update_board(self, event):
        exclude = event["exclude"]
        self.send(text_data=json.dumps({
            'type':'update_board',
            'exclude' : exclude
        }))
    def disconnect(self, close_code):
      print(f'Connection closed: {close_code}')
      async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)