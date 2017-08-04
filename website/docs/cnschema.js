$(document).ready(function() {
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
});
