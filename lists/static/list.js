
jQuery(document).ready(function(){
  $('input').on('keypress', function(){
    $('.has-error').hide();
  });

  $('#id_text').on('focus', function(){
    $('.has-error').hide();
  })
})
