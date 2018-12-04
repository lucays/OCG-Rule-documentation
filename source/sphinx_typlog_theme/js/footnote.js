$(function() {
  $('a.footnote-reference').on('click', function(e) {
    e.preventDefault();
    var id = $(this).attr('href');
    var html = $(id).find('td.label + td').html();

    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    var style = 'top:' + e.pageY + 'px;';
    if (w > 560) {
      style += 'width:480px;';
      if (e.pageX > 240 && e.pageX + 240 < w) {
        style += 'left:' + (e.pageX - 240) + 'px;';
      } else if (e.pageX <= 240) {
        style += 'left:20px;';
      } else {
        style += 'right:20px;';
      }
    }
    showFootnote(html, style);
  });

  function showFootnote(html, style) {
    var CONTENT_ID = 'typlog-footnote-content';
    var content = document.getElementById(CONTENT_ID);
    if (!content) {
      content = document.createElement('div');
      content.id = CONTENT_ID;
      $('.body').append(content);
    }
    var MASK_ID = 'typlog-footnote-mask';
    var mask = document.getElementById(MASK_ID);
    if (!mask) {
      mask = document.createElement('div');
      mask.id = MASK_ID;
      document.body.appendChild(mask);
      mask.addEventListener('click', function () {
        content.className = '';
        mask.className = '';
      });
    }

    content.innerHTML = html;
    content.setAttribute('style', style);
    content.className = 'Active';
    mask.className = 'Active';
  }
});
