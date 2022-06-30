$(document).ready(function () {
    $('a[href^="http://"], a[href^="https://"], a[href^="/zh_CN"]').not('a[class*=internal]').attr('target', '_blank');
});