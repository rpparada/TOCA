

parToca = {
    'diasNuevoTocata': 7,
    'diasNuevoArtista': 30,
    'muestraTocatas': 10,
    'muestraArtistas': 4,
    'valoresEvaluacion': [
        (1,'Muy Mala'),
        (2,'Mala'),
        (3,'Regular'),
        (4,'Buena'),
        (5,'Muy Buena')
    ],
    'defaultEvaluacion': 3,
    # Parametros Artistas
    # Estado artista
    'disponible': 'DI',
    'noDisponible': 'ND',
    # Parametros Tocatas
    # Tipo tocata
    'cerrada': 'CE',
    'abierta': 'AB',
    # Estado tocata
    'inicial': 'IN',
    'publicado': 'PU',
    'suspendido': 'SU',
    'aplazado': 'AP',
    'confirmado': 'CN',
    'completado': 'CM',
    # Paginacion tocatas_vista
    'tocatas_pag': 4,
}

parArtistas = {
    'estado_tipos': [
        (parToca['disponible'], 'Disponible'),
        (parToca['noDisponible'], 'No Disponible'),
    ],
}

parTocatas = {
    'lugar_def_tipos': [
        (parToca['cerrada'],'Cerrada'),
        (parToca['abierta'],'Abierta'),
    ],
    'estado_tipos': [
        (parToca['inicial'], 'Inicial'),
        (parToca['publicado'], 'Publicado'),
        (parToca['suspendido'], 'Suspendido'),
        (parToca['aplazado'], 'Aplazado'),
        (parToca['confirmado'], 'Confirmado'),
        (parToca['completado'], 'Completado'),
    ]
}
