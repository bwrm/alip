$(function () {

  $("#list-view-btn").click(function () {
    $("#table-view").hide();
    $(".list-hidden").css("display", "block")

  });
  $("#table-view-btn").click(function () {
    $(".list-hidden").hide();
    $("#table-view").show();
  });
});
$(function () {
  var first_name=$.trim($("#id_first_name").val());
  var last_name=$.trim($("#id_last_name").val());
  var company=$.trim($("#id_company").val());
  var phone=$.trim($("#id_phone_number").val());
  var locality=$.trim($("#id_locality").val());
  var postal=$.trim($("#id_postal_code").val());
  var country=$.trim($("#id_country").val());
  var location=$.trim($("#id_location").val());


  if(first_name.length>0){
    $("#id_first_name").css("display","none");
    $("#first_name").append('<button type="button" class="btn btn-link" id="pencil-edit"> '+first_name+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(last_name.length>0){
    $("#id_last_name").css("display","none");
    $("#last_name").append('<button type="button" class="btn btn-link" id="pencil-edit1"> '+last_name+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(company.length>0){
    $("#id_company").css("display","none");
    $("#company").append('<button type="button" class="btn btn-link" id="pencil-edit2"> '+company+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(phone.length>0){
    $("#id_phone_number").css("display","none");
    $("#phone_number").append('<button type="button" class="btn btn-link" id="pencil-edit3"> '+phone+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(locality.length>0){
    $("#id_locality").css("display","none");
    $("#locality").append('<button type="button" class="btn btn-link" id="pencil-edit4"> '+locality+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(postal.length>0){
    $("#id_postal_code").css("display","none");
    $("#postal_code").append('<button type="button" class="btn btn-link" id="pencil-edit5"> '+postal+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(country.length>0){
    $("#id_country").css("display","none");
    $("#country").append('<button type="button" class="btn btn-link" id="pencil-edit6"> '+country+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }
  if(location.length>0){
    $("#id_location").css("display","none");
    $("#location").append('<button type="button" class="btn btn-link" id="pencil-edit7"> '+location+' <i class="glyphicon glyphicon-pencil"></i> </button>');
  }  
  

});
$(function () {

  $("#pencil-edit").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit1").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit2").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit3").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit4").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit5").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit6").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });

  $("#pencil-edit7").click(function () {
    $(this).append(fieldname);
    var fieldname=$(this).parent().attr('id');
    $(this).append(fieldname);
    $("#id_"+fieldname).css("display","block");
    $(this).hide();
  });
});