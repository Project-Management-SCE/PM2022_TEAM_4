$(function(){ 							   

	// radiys box
	$('.menu_nav ul li a').css({"border-radius": "8px", "-moz-border-radius":"8px", "-webkit-border-radius":"8px"});
	$('.sb_menu li a, .ex_menu li a').css({"border-radius": "15px", "-moz-border-radius":"15px", "-webkit-border-radius":"15px"});
	$('.mainbar .spec a').css({"border-radius": "10px", "-moz-border-radius":"10px", "-webkit-border-radius":"10px"});
	$('.pagenavi a, .pagenavi .current').css({"border-radius": "5px", "-moz-border-radius":"5px", "-webkit-border-radius":"5px"});
	
});
$(document).ready(function(){
  $('.story').owlCarousel({
    center: false,
    items:3,
    loop:true,
    margin:5,
	 stagePadding: 15,

});
});
$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
function scrollDown() {
  var focusBottom = document.getElementById("adobewordpress");
  focusBottom.scrollTop = focusBottom.scrollHeight;
}

$("input").keypress(function(event) {
  if (event.which == 13) {
    event.preventDefault();
    $('form.chat input[type="submit"]').click();
  }
});
$('form.chat input[type="submit"]').click(function(event) {
  event.preventDefault();
  var message = $('form.chat input[type="text"]').val();
  if ($('form.chat input[type="text"]').val()) {
    var d = new Date();
    var clock = d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var currentDate =
      (("" + day).length < 2 ? "0" : "") +
      day +
      "." +
      (("" + month).length < 2 ? "0" : "") +
      month +
      "." +
      d.getFullYear() +
      "&nbsp;&nbsp;" +
      clock;
    $("form.chat div.messages").append(
      '<div class="message"><div class="myMessage"><p>' +
        message +
        "</p><date>" +
        currentDate +
        "</date></div></div>"
    );
    setTimeout(function() {
      $("form.chat > span").addClass("spinner");
    }, 100);
    setTimeout(function() {
      $("form.chat > span").removeClass("spinner");
    }, 2000);
  }
  $('form.chat input[type="text"]').val("");
  scrollDown();
});

/* DEMO */
if (parent == top) {
  $("a.article").show();
}
