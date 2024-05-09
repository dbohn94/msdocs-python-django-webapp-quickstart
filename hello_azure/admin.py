from django.contrib import admin

from .models import DecisionLog, DecisionSummary, TradeLog


admin.site.register(DecisionLog)
admin.site.register(DecisionSummary)
admin.site.register(TradeLog)
