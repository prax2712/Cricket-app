from django.contrib import admin
from .models import player_stats, match_info, innings, player_match_stats,innings,overs_timeline  # Import all your models


admin.site.register(match_info)
admin.site.register(innings)
admin.site.register(player_match_stats)
admin.site.register(player_stats)
admin.site.register(overs_timeline)
