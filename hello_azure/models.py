from django.db import models
from django.utils.translation import gettext_lazy as _


class DecisionLog(models.Model):
    class Decision(models.TextChoices):
        DO_NOTHING = "DO_NOTHING", _("Do nothing")
        BUY = "BUY", _("Buy")
        SELL = "SELL", _("Sell")

    class Reason(models.TextChoices):
        MARKET_CLOSED = "MARKET_CLOSED", _("Market closed")
        SMA1_GT_SMA2 = "SMA1_GT_SMA2", _("SMA1 > SMA2")
        SMA2_GT_SMA1 = "SMA2_GT_SMA1", _("SMA2 > SMA1")
        NO_CROSSOVER = "NO_CROSSOVER", _("No crossover")
        ALREADY_OPEN = "ALREADY_OPEN", _("Already have an open position")

    timestamp = models.DateTimeField(auto_now_add=True)

    stock = models.CharField(max_length=10)

    decision = models.CharField(choices=Decision.choices, max_length=20)

    reason = models.CharField(choices=Reason.choices, max_length=20)


class TradeLog(models.Model):
    class Action(models.TextChoices):
        BUY = "BUY", _("Buy")
        SELL = "SELL", _("Sell")

    timestamp = models.DateTimeField(auto_now_add=True)

    stock = models.CharField(max_length=10)

    action = models.CharField(choices=Action.choices, max_length=20)

class DecisionSummary(models.Model):
    # Define your fields here. The field names should match the column names of your view.
    # For example:
    timestamp = models.DateTimeField(auto_now_add=True)
    stock = models.CharField(max_length=10)
    decision = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)