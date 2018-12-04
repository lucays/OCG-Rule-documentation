$(function() {
  var href = $('.github').attr('href');
  var repo = href.replace('https://github.com/', '');

  function fetchRepo (repo) {
    var url = 'https://api.github.com/repos/' + repo;
    $.getJSON(url, function (data) {
      var counts = [+new Date(), data.stargazers_count, data.forks_count];
      localStorage.setItem('gh:' + repo, JSON.stringify(counts));
      update(counts[1], counts[2]);
    });
  }

  var cache = localStorage.getItem('gh:' + repo);
  if (cache) {
    try {
      var counts = JSON.parse(cache);
      update(counts[1], counts[2]);
      var delta = new Date() - counts[0];
      if (delta < 0 || delta > 900000) {
        fetchRepo(repo);
      }
    } catch (error) {
      fetchRepo(repo);
    }
  } else {
    fetchRepo(repo);
  }

  function update (stars, forks) {
    $('.github_stars strong').text(stars);
    $('.github_forks strong').text(forks);
  }
});
