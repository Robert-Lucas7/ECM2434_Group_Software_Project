from django.contrib import admin
from .models import Village, VillageShop, CustomUser, DailyChallenge

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    pass

@admin.register(VillageShop)
class VillageShopAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    pass

