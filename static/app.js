$(document).ready(function() {
    var $checkbox = $("#fixed-width-toggle");
    var $navbar = $("#top-navbar");
    var $container = $("#content-container");

    $checkbox.change(function() {
	if($checkbox.is(":checked")) {
	    $navbar.addClass("full");
	    $container.addClass("full");
	} else {
	    $navbar.removeClass("full");
	    $container.removeClass("full");
	}
    });
});
