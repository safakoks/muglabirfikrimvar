
// Beğenme
$(".like-btn").click(function(){
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
})



var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],
  onBeforePageLoad: function () {
    $('.loading').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading').hide();
  }
});
// Sayfalama
