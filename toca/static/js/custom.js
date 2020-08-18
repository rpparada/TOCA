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

// Al cargar la pagina deja el foco en el primer campo del formulario
$(document).ready(function(){
  $( "#primercampo" ).focus();
})

// Valida campos formulario antes de enviarlo a servidor
$("#formtocheck").submit(function(){

  // verifica campos requeridos vacios
  var isFormValid = true;
  var setfocus = true
  $(".requerido").each(function(){
      if ($.trim($(this).val()).length == 0){
          $(this).addClass("destacaerrorform");
          isFormValid = false;
          if (setfocus) {
            $(this).focus();
            setfocus = false;
          }
      }
      else{
          $(this).removeClass("destacaerrorform");
      }
  });

  if (!isFormValid) {
    $("#mensajerror").text("Completa los campos destacados");
    $("#mensajerror").removeAttr('hidden');
  };

  // Valida que ambas contraseñas sen iguales
  if (isFormValid){
    var pass = $('input[name=password1]');
    var repass = $('input[name=password2]');

    if (pass.val() != repass.val()) {
      pass.val('');
      repass.val('');
      pass.focus();

      $("#mensajerror").text("Ambas contraseñas deben ser iguales");
      $("#mensajerror").removeAttr('hidden');

      isFormValid = false;
    } else {
      $("#mensajerror").empty();
      $("#mensajerror").attr('hidden');
    }
  }


  // verifica rut con digito verificador
  if (isFormValid){
    digver = $("#digitover").val();
    rut = $("#rut").val();
    if (digver && rut) {
      var digver, rut, M, S, final;
      M=0,S=1;

      for (;rut;rut=Math.floor(rut/10)) {
        S=(S+rut%10*(9-M++%6))%11;
      }
      final = S?S-1:'K';

      if (final!=digver){
        $("#digitover").addClass("destacaerrorform");
        $("#rut").focus();
        $("#mensajerror").text("Error en digito verificador");
        $("#mensajerror").removeAttr('hidden');
        isFormValid = false;
      } else {
        $("#mensajerror").empty();
        $("#mensajerror").attr('hidden');
      }
    }
  }

  // validaciones formulario de tocatas
  // asistentes_max tiene que ser mayor que asistentes_min
  if (isFormValid) {
    asis_min = $('input[name=asistentes_min]');

    if (parseInt(asis_min.val()) <= 0) {
      asis_min.focus();
      $("#mensajerror").text("Asistencia Mínima debe ser mayor a 0.");
      $("#mensajerror").removeAttr('hidden');
      isFormValid = false;
    } else {
      $("#mensajerror").empty();
      $("#mensajerror").attr('hidden');
    }
  }

  return isFormValid;
});

$(document).ready(function(){

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

  // Agregar o quitar tocatas de carro y actualizar
  var tocataForm = $(".form-tocata-ajax");
  tocataForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    //var actionEndpoint = thisForm.attr("action");
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
    var carroTable = $(".carro-table");
    var carroTableRes = $(".carro-table-res");

    var carroBody = carroTable.find(".carro-body");
    var tocataRows = carroBody.find(".carro-tocata")

    var carroResumen = carroTableRes.find(".carro-resumen");

    var currentUrl = window.location.href

    var updateCarroUrl = "api/carro";
    var updateCarroMethod = "GET";
    var data = {};
    $.ajax({
      url: updateCarroUrl,
      method: updateCarroMethod,
      data: data,
      success: function(data){
        var formQuitarTocataCarro = $(".form-quitar-carro-home")
        if (data.tocatas.length > 0) {
          tocataRows.html(" ")
          $.each(data.tocatas, function(index, value){
            var nuevoCarroTocataQuitar = formQuitarTocataCarro.clone()
            nuevoCarroTocataQuitar.css("display","block")
            nuevoCarroTocataQuitar.find(".carro-tocata-id").val(value.id)
            carroBody.prepend("<tr class=\"carro-tocata\"><td class=\"cart-product-remove\">"+nuevoCarroTocataQuitar.html()+"</td><td class=\"cart-product-name\"><span><a href='"+value.url+"'>"+value.nombre+"</a></span></td><td class=\"cart-product-subtotal\"><span class=\"amount\">$"+value.costo+"</span></td></tr>")
          })
          carroResumen.find(".carro-subtotal").text(data.subtotal)
          carroResumen.find(".carro-total").text(data.total)
        } else {
          window.location.href = currentUrl
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


})
