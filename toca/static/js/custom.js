/*

1. Add your custom JavaScript code below
2. Place the this code in your template:

*/

setTimeout(function(){
  $('.bootstrap-notify').fadeOut('slow');
}, 2000);

$('.close').click(function () {
  $('.bootstrap-notify').fadeOut();
});
