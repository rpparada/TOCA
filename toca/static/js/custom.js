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

  if (window.location.pathname === "/lugares/agregarlugar"){
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

  } else if (window.location.pathname === "/tocatas/artista/creartocata") {
    // Creacion de Tocatas
    // Define variables iniciales
    var opcione = $("#checklugar").val();

    if (opcione === "No tienes lugares registrados") {
      $('select[name=lugar_def] option:eq(1)').attr('selected', 'selected');
      $('select[name=lugar_def]').prop('disabled', true);
      $('#opcionestipo').prop('disabled', true);
      $('#opcionesregion').prop('disabled', false);
      $('#opcionescomuna').prop('disabled', false);
    } else {
      $('#opcionestipo').prop('disabled', false);
      $('#opcionesregion').prop('disabled', true);
      $('#opcionescomuna').prop('disabled', true);
    }

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
  if (window.location.pathname === "/lugares/agregarlugar"){
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
// Habilita campos de acuerdo con el tipo de tocata
$("#tipotocata").change(function () {

  var tipotocata = $(this).val();

  if (tipotocata == 'AB') {
    $('#opcionestipo').prop('disabled', true);
    $('#opcionesregion').prop('disabled', false);
    $('#opcionescomuna').prop('disabled', false);
  } else if (tipotocata == 'CE') {
    $('#opcionestipo').prop('disabled', false);
    $('#opcionesregion').prop('disabled', true);
    $('#opcionescomuna').prop('disabled', true);
  }
});

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
    $("#mensajerror").text("Completa los campos detacados");
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
  if (isFormValid) {

  }

  return isFormValid;
});
