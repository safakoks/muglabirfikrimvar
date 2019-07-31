
// Beğenme

$('body').on('click', ".idea-card button.like-btn", function() {
    elem = $(this)
    var ideaID = elem.val()
    $.ajax({
        url: '/begen/',
        data: {
          'ideaID': ideaID
        },
        dataType: 'json',
        success: function (data) {
          if (data.status) {
            elem.children(".like-count").html(data.likecount)
          }
        }
      });
});


var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],

  onBeforePageLoad: function () {
    $('.loading').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading').hide();
  }
});

var infinite2 = new Waypoint.Infinite({
  element: $('.infinite-container2')[0],
  more: '.infinite-more-link2',
  items: '.infinite-item2',
  onBeforePageLoad: function () {
    $('.loading2').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading2').hide();
  }
});

