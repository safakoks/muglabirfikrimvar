
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