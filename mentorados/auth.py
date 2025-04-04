from .models import Mentorado

def validate_token(token):
    return Mentorado.objects.filter(token=token).first()