/**
*
* -------------------------------------------------
*
* Template : Future - Coming Soon HTML5 Template
* Author : thecodrops
* Author URI : http://thecodrops.com
*
* --------------------------------------------------
*
**/


jQuery(document).ready(function () {    
	'use strict';	
	// Cowndown Timer
    $('.tc-count-down').countdown('2018/10/10', function(event) {
        var $this = $(this).html(event.strftime(''
        + '<span class="c-grid"> <span class="c-value">%D</span> <span class="c-title">days</span> </span> '
        + '<span class="c-grid"> <span class="c-value">%H</span> <span class="c-title">hours</span> </span> '
        + '<span class="c-grid"> <span class="c-value">%M</span> <span class="c-title">minutes</span> </span> '
        + '<span class="c-grid"> <span class="c-value">%S</span> <span class="c-title">seconds</span> </span> '));
    });
});
