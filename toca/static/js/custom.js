/*
1. Add your custom JavaScript code below
2. Place the this code in your template:
*/

/* Notificaciones */
// Fadeout sobre notificacion popup
setTimeout(function(){
  $('.bootstrap-notify').fadeOut('slow');
}, 5000);

$('.close').click(function () {
  $('.bootstrap-notify').fadeOut();
});

// Acciones cuando paguinas cargan
$(document).ready(function (){

  if (window.location.pathname === "/lugares/agregarlugar" || window.location.pathname === "/carro/checkout/"){
    // Agregar Lugar
    // Define posibles comunas de acuerdo a region seleccionada
    // Habilita campos de acuerdo con el tipo de tocata
    var url = $("#formtocheck").attr("data-ciudad-url-agregar");
    var regionId = $("#id_region").val();

    $.ajax({
      url: url,
      data: {
        'region': regionId
      },
      success: function (data) {
        $("#id_comuna").html(data);
      }
    });

  } else if (!window.location.pathname.search("/lugares/milugar_")){
    // Actualizacion lugar
    // Define posibles comunas de acuerdo a region seleccionada
    // Habilita campos de acuerdo con el tipo de tocata
    var url = $("#formtocheck").attr("data-ciudad-url-actualizar");
    var regionId = $("#id_region_ajax").val();
    var comunaId = $("#id_comuna_ajax").val();

    $.ajax({
      url: url,
      data: {
        'region': regionId,
        'comuna': comunaId,
      },
      success: function (data) {
        $("#id_comuna").html(data);
      }
    });

  } else if (window.location.pathname === "/tocatas/artista/creartocataabierta") {
    // Creacion de Tocatas
    // Define variables iniciales
    var url = $("#formtocheck").attr("data-ciudad-url-agregar");
    var regionId = $("#opcionesregion").val();

    $.ajax({
      url: url,
      data: {
        'region': regionId
      },
      success: function (data) {
        $("#opcionescomuna").html(data);
      }
    });
  }
});

// Define posibles comunas de acuerdo a region seleccionada
$("#id_region").change(function () {
  if (window.location.pathname === "/lugares/agregarlugar" || window.location.pathname === "/carro/checkout/" ){
    var url = $("#formtocheck").attr("data-ciudad-url-agregar");
    var regionId = $(this).val();
    $.ajax({
      url: url,
      data: {
        'region': regionId
      },
      success: function (data) {
        $("#id_comuna").html(data);
      }
    });
  } else if (!window.location.pathname.search("/lugares/milugar_")){
    var url = $("#formtocheck").attr("data-ciudad-url-actualizar");
    var regionId = $("#id_region").val();
    var comunaId = $("#id_comuna").val();

    $.ajax({
      url: url,
      data: {
        'region': regionId,
        'comuna': comunaId,
      },
      success: function (data) {
        $("#id_comuna").html(data);
      }
    });
  }
});

/* Creacion de Tocatas */
// Define posibles comunas de acuerdo a region seleccionada
$(document).on('change','#opcionesregion', function () {
  var url = $("#formtocheck").attr("data-ciudad-url-agregar");
  var regionId = $(this).val();
  $.ajax({
    url: url,
    data: {
      'region': regionId
    },
    success: function (data) {
      $("#opcionescomuna").html(data);
    }
  });
});

$(document).ready(function(){

  // Agregar o quitar tocatas de carro y actualizar
  var tocataForm = $(".form-tocata-ajax");
  console.log(tocataForm);
  tocataForm.submit(function(event){
    console.log("test1");
    event.preventDefault();
    // event.stopPropagation();
    console.log("test2");
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-span")
        if (data.added){
          submitSpan.html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Quitar</button>")
        } else {
          submitSpan.html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Agregar</button>")
        }
        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
        if(window.location.href.indexOf("carro") != -1) {
          actualizaCarro()
        }
      },
      error: function(errorData){
        $.alert({
          title: "TI Error",
          content: "Algo paso",
          theme: "modern"
        })
      }
    })
  })

  function actualizaCarro(){
    var currentUrl = window.location.href
    var updateCarroUrl = "api/carro";
    var updateCarroMethod = "GET";
    var data = {};
    $.ajax({
      url: updateCarroUrl,
      method: updateCarroMethod,
      data: data,
      success: function(data){
        if (!$.trim(data)){
          window.location.href = currentUrl;
        } else {
          $(".bodycarroupdate").html(data);
        }
      },
      error: function(errorData){
        $.alert({
          title: "TI Error",
          content: "Algo paso",
          theme: "modern"
        })
      }
    })
  }

  // Controla cantidad de elemento a agregar en carro
  var numItemCarro = $(".cart-product-quantity");
  var botonmenos = numItemCarro.find(".minus");
  var botonmas = numItemCarro.find(".plus");
  var textCantidad = numItemCarro.find(".qty");

  botonmas.click(function(event) {
    var cantidadActual = parseInt(textCantidad.val());
    if (cantidadActual < 2) {
      textCantidad.val(cantidadActual+1);
    }
  });

  botonmenos.click(function(event) {
    var cantidadActual = parseInt(textCantidad.val());
    if (cantidadActual > 1) {
      textCantidad.val(cantidadActual-1);
    }
  });

  // Busqueda actomatica
  // var searchForm = $(".search-form");
  // var searchInput = searchForm.find("[name='q']");
  // var searchBtn = searchForm.find("[type='submit']")
  // var typingTimer;
  // var typingInterval = 500;
  // searchInput.keyup(function(event){
  //   clearTimeout(typingTimer)
  //   typingTimer = setTimeout(ejecutaBusqueda,typingInterval);
  // })
  // searchInput.keydown(function(event){
  //   clearTimeout(typingTimer)
  // })
  //
  // function ejecutaBusqueda(){
  //   var query = searchInput.val();
  //   window.location.href="/busqueda/?q="+query
  // }
})
