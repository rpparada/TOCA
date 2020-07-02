from rest_framework import serializers
from artista.models import Artista

#serilaizer
class pagination_ser(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Artista #model 
