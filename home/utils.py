from usuario.models import Usuario
from cobro.models import Carro

from toca.parametros import parToca

def getDataHeadIndex(request):

    # Usuario Artista Header
    if request.user.is_authenticated:
        usuario = Usuario.objects.filter(user=request.user)[0]
        numitemscarro = Carro.objects.filter(usuario=request.user).filter(estado=parToca['pendiente']).count()
    else:
        usuario = None
        numitemscarro = 0

    return usuario, numitemscarro
