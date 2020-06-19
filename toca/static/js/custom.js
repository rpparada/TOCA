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

/* Creacion de Tocatas */
// Define posibles comunas de acuerdo a region seleccionada
// Habilita campos de acuerdo con el tipo de tocata
$("#tipotocata").change(function () {

  var tipotocata = $(this).val();

  if (tipotocata == 'AB') {
    $('#opcionestipo').off();
    $('#opcionestipo').prop('disabled', true);
    $('#opcionestipo').val('');

    $('#opcionesregion').prop('disabled', false);
    $('#opcionesregion').val($("#opcionesregion option:first").val())

    $('#opcionescomuna').prop('disabled', false);
    $('#opcionescomuna').val($("#opcionescomuna option:first").val())

    var url = $("#tocataForm").attr("data-ciudad-url-agregar");
    var regionId = $('#opcionesregion').val();

    $.ajax({
      url: url,
      data: {
        'region': regionId
      },
      success: function (data) {
        $("#opcionescomuna").html(data);
      }
    });

  } else if (tipotocata == 'CE') {
    $('#opcionestipo').prop('disabled', false);
    $('#opcionestipo').val($("#opcionestipo option:first").val());

    $('#opcionesregion').off();
    $('#opcionesregion').prop('disabled', true);
    $('#opcionesregion').val($("#opcionesregion option:first").val());

    $('#opcionescomuna').off();
    $('#opcionescomuna').prop('disabled', true);
    $('#opcionescomuna').val($("#opcionescomuna option:first").val());
  }
});

// Define posibles comunas de acuerdo a region seleccionada
$(document).on('change','#opcionesregion', function () {
  var url = $("#tocataForm").attr("data-ciudad-url-agregar");
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

$(document).ready(function (){

  if (window.location.pathname === "/lugares/agregarlugar"){
    // Agregar Lugar
    // Define posibles comunas de acuerdo a region seleccionada
    // Habilita campos de acuerdo con el tipo de tocata
    $('#opcionestipo').prop('disabled', false);
    $('#opcionestipo').val($("#opcionestipo option:first").val());

    $('#opcionesregion').off();
    $('#opcionesregion').prop('disabled', true);
    $('#opcionesregion').val($("#opcionesregion option:first").val());

    $('#opcionescomuna').off();
    $('#opcionescomuna').prop('disabled', true);
    $('#opcionescomuna').val($("#opcionescomuna option:first").val());

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
  return isFormValid;
});
