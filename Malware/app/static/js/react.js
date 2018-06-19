function clear(query,area) {
  $(query).val('');
  $(area).html('');
}
function contentBlock(title,desc,link) {
  var block = "<div class = \"animated fadeIn content-block text-responsive\"> \
          <blockquote> \
            <h3 class = \"title-text\" id = \"titleText\">"+title+"</h3> \
            <span class = \"description\" id = \"description\">"+desc+"</span> \
            <caption class = \"link\"><a href='"+link+"'>More Info</a></caption> \
          </blockquote> \
        </div>"
        return block;
}

function search(query) {
  var API_URL = "https://en.wikipedia.org/w/api.php";
  if(query.value != "") {
    var data;
    $.ajax({
      
      url : API_URL,
      jsonp : "callback",
      dataType : 'jsonp',
      data : {
        action : "opensearch",
        search : query.value,
        format : "json",
        limit : "10"
      },
      xhrFields : {
        onreadystatechange : function() {

   $("#contentArea").html("Getting Knowledge");
   }
      },
      type : "POST",
      headers: { 'Api-User-Agent': 'knowledge-center/1.0' },
      success : function(data) {
        console.log(data);
        $('#contentArea').html("");
        $(".input-area").css("margin-top","5%");
        for(i = 0;i<data[1].length;i++) {
          console.log(i);
          console.log(data[1][i],data[2][i],data[3][i]);
          $('#contentArea').append(contentBlock(data[1][i],data[2][i],data[3][i]));
        }
      },
      

    });
    
  }
  else {
    $("#contentArea").html("<span style = \"font-size : 20px\" class='animated fadeInUp'>Empty Input</span>");
  }
  
}