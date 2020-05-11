/*

1. Add your custom JavaScript code below
2. Place the this code in your template:

*/

/* Notificaciones */
setTimeout(function(){
  $('.bootstrap-notify').fadeOut('slow');
}, 2000);

$('.close').click(function () {
  $('.bootstrap-notify').fadeOut();
});

/* Creacion de Tocatas */
$("#tipotocata").change(function () {
  var tipotocata = $(this).val();

  if (tipotocata == 'AB') {
    $('#opcionestipo').off();
    $('#opcionestipo').prop('disabled', true);
    $('#opcionestipo').val('');
  } else if (tipotocata == 'CE') {
    $('#opcionestipo').prop('disabled', false);
    $('#opcionestipo').val($("#opcionestipo option:first").val())
  }

});

$(document).ready(function () {

  console.log("hola");

    $('#datetimepicker1').datetimepicker();

    $('#datetimepicker2').datetimepicker({
        format: 'L'
    });

    $('#datetimepicker3').datetimepicker({
        format: 'LT'
    });

    $('#datetimepicker5').datetimepicker();

    $('#datetimepicker6').datetimepicker({
        defaultDate: "11/1/2019",
        disabledDates: [
            moment("12/25/2019"),
            new Date(2019, 11 - 1, 21),
            "11/25/2019 00:53",
            "11/26/2019 00:53",
            "11/27/2019 00:53",
            "11/28/2019 00:53"
        ]
    });

    $('#datetimepicker7').datetimepicker();
    $('#datetimepicker8').datetimepicker({
        useCurrent: false
    });
    $("#datetimepicker7").on("change.datetimepicker", function (e) {
        $('#datetimepicker8').datetimepicker('minDate', e.date);
    });
    $("#datetimepicker8").on("change.datetimepicker", function (e) {
        $('#datetimepicker7').datetimepicker('maxDate', e.date);
    });

    $('#datetimepicker9').datetimepicker({
        icons: {
            time: "fa fa-clock",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        }
    });
    $('#datetimepicker10').datetimepicker({
        viewMode: 'years'
    });
    $('#datetimepicker11').datetimepicker({
        viewMode: 'months',
    });
    $('#datetimepicker12').datetimepicker({
        daysOfWeekDisabled: [0, 6]
    });

    $('#datetimepicker13').datetimepicker({
        inline: true,
        format: 'L'
    });

    $('#datetimepicker13_1').datetimepicker({
        inline: true,
        format: 'LT'
    });

    $('#datetimepicker14').datetimepicker({
        allowMultidate: true,
        multidateSeparator: ','
    });


    //Modal examples
    $('#datetimepicker1_modal').datetimepicker();

    $('#datetimepicker2_modal').datetimepicker({
        format: 'L'
    });

    $('#datetimepicker3_modal').datetimepicker({
        format: 'LT'
    });

});
