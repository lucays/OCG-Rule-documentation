$(document).ready(function () {
    $('a[href^="http://"], a[href^="https://"], a[href^="/zh_CN"]').not('a[class*=internal], a[href^="#id"]').attr('target', '_blank');
});