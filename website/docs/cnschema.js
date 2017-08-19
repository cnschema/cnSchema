$(document).ready(function() {
  // add navigation bar
  $('#leftNav li span').click(function(){
    $('#leftNav li span').removeClass('active');
    $(this).addClass('active');
    var index = $(this).parent().index();
    $("#rightBox > ul > li").hide();
    $("#rightBox > ul > li").eq(index).show();
  });
  $('#rightBox .examples-top > ul > li').click(function() {
    $('#rightBox .examples-top > ul > li').removeClass('active');
    $(this).addClass('active');
    var index = $(this).index();
    $("#rightBox .examples-bottom > ul >li ").hide();
    $("#rightBox .examples-bottom > ul >li").eq(index).show();
  });
  $("#aboutLeft > ul >li").click(function() {
    $('#aboutLeft > ul > li > span').removeClass('active');
    $(this).children().addClass('active');
    var index = $(this).index();
    $('#aboutContent > ul>li').hide();
    $("#aboutContent >ul >li").eq(index).show();
  })

  // add autocomplete
  $( "#autocomplete_term" ).autocomplete({
    source: function(request, response) {
        $.getJSON("http://cnschema.org:18080/autocomplete",
            { q: $('#autocomplete_term').val() },
            function(result){
                //console.log(JSON.stringify(result));
                response($.map(result.results, function(item) {
                  return item
                }))
            })
      },
      minLength: 1
    }).data("ui-autocomplete")._renderItem = function (ul, item) {
      link = '<a href="'+item["@id"]+'">'+item.name+' ('+item.nameZh+')</a>';
      //console.log(link);
      return $("<li class='auto-complete-li'></li>")
        .data("item.autocomplete", item)
        .append(link)
        .appendTo(ul);
    };
});
