

parToca = {
    'diasNuevoTocata': 7,
    'diasNuevoArtista': 30,
    'muestraTocatas': 3,
    'muestraArtistas': 3,
    'valoresEvaluacion': [
        (0,'No Evaluada'),
        (1,'Muy Mala'),
        (2,'Mala'),
        (3,'Regular'),
        (4,'Buena'),
        (5,'Muy Buena')
    ],
    'defaultEvaluacion': 0,
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
    'borrado': 'BO',
    # Paginacion tocatas_vista
    'tocatas_pag': 4,
    'bancoDefecto': '012',
    'tipoCuentaDefecto': '001',
    'prefijoCelChile': '(+56) 9 ',
    # Ciudad por defecto
    'cuidadDefecto': 'Santiago',
    'paisDefecto': 'Chile',
    # Lugares Tocatas
    'elegido': 'EL',
    'noelegido': 'NE',
}

parLugaresToc = {
    'estado_lugartocata': [
        (parToca['elegido'], 'Elegido'),
        (parToca['noelegido'], 'No Elegido')
    ]
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
        (parToca['borrado'], 'Borrado'),
    ],
    'estado_tipos_vista': [
        parToca['inicial'],
        parToca['publicado'],
        parToca['suspendido'],
        parToca['aplazado'],
        parToca['confirmado'],
        parToca['completado'],
    ],

}

parUsuarioArtistas = {
    'bancos': [
        ('012','BANCO DEL ESTADO DE CHILE'),
        ('001','BANCO DE CHILE'),
        ('009','BANCO INTERNACIONAL'),
        ('014','SCOTIABANK CHILE'),
        ('016','BANCO DE CREDITO E INVERSIONES'),
        ('028','BANCO BICE'),
        ('031','HSBC BANK (CHILE)'),
        ('037','BANCO SANTANDER-CHILE'),
        ('039','ITAÚ CORPBANCA'),
        ('049','BANCO SECURITY'),
        ('051','BANCO FALABELLA'),
        ('053','BANCO RIPLEY'),
        ('055','BANCO CONSORCIO'),
        ('504','SCOTIABANK AZUL (ex BANCO BILBAO VIZCAYA ARGENTARIA, CHILE (BBVA))'),
        ('059','BANCO BTG PACTUAL CHILE'),
    ],
    'tipo_cuenta': [
        ('001','Cuenta Corriente'),
        ('002','Cuenta de Ahorro'),
        ('003','Cuenta Vista'),
        ('004','Cuenta Chequera Electrónica'),
        ('005','Cuenta RUT'),
    ]
}

parLugares = {
    'estado_tipos': [
        (parToca['disponible'], 'Disponible'),
        (parToca['noDisponible'], 'No Disponible'),
    ],
}
