from django.conf import settings

def hot_ui(request):
    return {"HOT_UI": settings.HOT_UI_VERSION, "WA": settings.WEBAWESOME_VERSION}