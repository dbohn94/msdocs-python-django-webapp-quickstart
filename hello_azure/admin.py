from django.contrib import admin

from .models import DecisionLog, TradeLog


admin.site.register(DecisionLog)
admin.site.register(TradeLog)
