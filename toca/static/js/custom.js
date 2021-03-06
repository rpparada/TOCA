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


  if ((window.location.href.indexOf("/lugares/agregarlugar") > -1) || (window.location.href.indexOf("/propuestaslugar/proponerlugar") > -1) || (window.location.href.indexOf("/tocatas/artista/seleccionardireccion/") > -1)){
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

  } else if (window.location.pathname === "/ofrecetucasa/artista/creartocataabierta") {
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

  if ((window.location.href.indexOf("/lugares/agregarlugar") > -1) || (window.location.href.indexOf("/propuestaslugar/proponerlugar") > -1) || (window.location.href.indexOf("/tocatas/artista/seleccionardireccion/") > -1)){
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

  var tablaCarro = $("#tablacarro")
  tablaCarro.on("submit",".form-tocata-ajax-carro", function() {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
        actualizaCarro()
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

  var tocataForm = $(".form-tocata-ajax");
  tocataForm.submit(function(event){
    event.preventDefault();
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
          $(".qty").val(1)
          // enable - and enable +
          $(".minus").prop( "disabled", false );
          $(".plus").prop( "disabled", false );
        } else {
          submitSpan.html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Agregar</button>")
          $(".qty").val(0)
          // disable - and enable +
          $(".minus").prop( "disabled", true );
          $(".plus").prop( "disabled", false );
        }
        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
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
        if (data.carroData) {
          $(".bodycarroupdate").replaceWith(data.html);
          $(".carro-subtotal").text(data.subtotal)
          $(".carro-total").text(data.total)
        } else {
          window.location.href = currentUrl;
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
  var cambiaNumItems = $(".cart-product-quantity")
  cambiaNumItems.on("submit",".form-carro-resta-ajax", function() {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    var currentUrl = window.location.href

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        // actualizar boton de agregar y control de cantidad
        if (data.origenTocata) {
          $(".quantity").replaceWith(data.html);
          if (data.removed){
            $(".submit-span").html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Agregar</button>")
          }
        } else if (data.carroData) {
          $(".bodycarroupdate").replaceWith(data.html);
          $(".carro-subtotal").text(data.subtotal)
          $(".carro-total").text(data.total)
        }
        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
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

  cambiaNumItems.on("submit",".form-carro-suma-ajax", function() {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    var currentUrl = window.location.href

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        // actualizar boton de agregar y control de cantidad
        if (data.origenTocata) {
          $(".quantity").replaceWith(data.html);
          if (data.added){
            $(".submit-span").html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Quitar</button>")
          }
        } else if (data.carroData) {
          $(".bodycarroupdate").replaceWith(data.html);
          $(".carro-subtotal").text(data.subtotal)
          $(".carro-total").text(data.total)
        }

        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
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

  tablaCarro.on("submit",".form-carro-resta-ajax", function() {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    var currentUrl = window.location.href

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        // actualizar boton de agregar y control de cantidad
        if (data.origenTocata) {
          $(".quantity").replaceWith(data.html);
          if (data.removed){
            $(".submit-span").html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Agregar</button>")
          }
        } else if (data.carroData) {
          if (data.carroNumItem !== 0) {
            $(".bodycarroupdate").replaceWith(data.html);
            $(".carro-subtotal").text(data.subtotal)
            $(".carro-total").text(data.total)
          } else {
            window.location.href = currentUrl;
          }
        }
        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
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

  tablaCarro.on("submit",".form-carro-suma-ajax", function() {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    var currentUrl = window.location.href

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        // actualizar boton de agregar y control de cantidad
        if (data.origenTocata) {
          $(".quantity").replaceWith(data.html);
          if (data.added){
            $(".submit-span").html("<button type='submit' class='btn'><i class='icon-shopping-cart'></i> Quitar</button>")
          }
        } else if (data.carroData) {
          if (data.carroNumItem !== 0) {
            $(".bodycarroupdate").replaceWith(data.html);
            $(".carro-subtotal").text(data.subtotal)
            $(".carro-total").text(data.total)
          } else {
            window.location.href = currentUrl;
          }
        }

        var navbarcarro = $(".navbar-carro-numitems")
        navbarcarro.text(data.carroNumItem)
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
