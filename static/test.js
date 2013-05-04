$(document).ready(function ($) {
        $('#tabs').tab();
        $('.dropdown-toggle').dropdown();
        $('.dropdown input, .dropdown label').click(function(e) {
    e.stopPropagation();
  });
    });
