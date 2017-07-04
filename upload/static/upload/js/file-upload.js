$(function () {

  $(".js-upload-files").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
      sequentialUploads: true,
      
          start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
      
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a><button type='submit' class='btn btn-danger pull-right'>\
      <span class='glyphicon glyphicon-trash'></span>\
    </button></td></tr>"
        )
      }
    }
  });

});

$(function () {

  $(".btn-danger").click(function () {
    var fileName=$(this).attr('name');
    var csrftoken = $(this).attr('data-form-data');
    $.post('/deletefile/', 'id=2&file='+fileName+'&'+'csrfmiddlewaretoken='+csrftoken);
    $(this).before("<span class=pull-right>Deleted</span>")
    $(this).hide();
  });

});

$(function () {

  $(".btn-save-form").click(function () {
    var csrftoken = $(this).attr('data-form-data');
    $.post('/finishcreating/', 'success=1&csrfmiddlewaretoken='+csrftoken);
    window.location.replace("/myaccount/myproducts");
  });

});