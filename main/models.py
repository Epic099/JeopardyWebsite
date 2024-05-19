from django.db import models
from django.contrib.auth.models import User
from . board import Board

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", blank=True, null=True)
    name = models.CharField(max_length=15)
    Points = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} | {self.name}"

# Create your models here.
class Lobby(models.Model):
    Lobby_id = models.CharField(max_length=8)
    users = models.ManyToManyField(Player, related_name="players")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host", blank=True, null=True)
    question = models.CharField(max_length=3, blank=True, null=True)
    buzzered_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    buzzered_time = models.CharField(max_length=30, blank=True, null=True)
    started_time = models.CharField(max_length=30, blank=True, null=True)
    board = models.JSONField(default=Board.randomBoard().to_JSON(), blank=True, null=True)
    def set_board(self, board : Board):
        self.board = board.to_JSON()
    def get_board(self):
        return Board.from_JSON(self.board)
    def __str__(self):
        return f"{self.host.username}´s lobby"