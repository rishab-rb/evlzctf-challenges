$.fn.extend({
    animateCss: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});

var apiURL = "https://andruxnet-random-famous-quotes.p.mashape.com/?cat=famous";
var quote;
$(document).ready(function() {
  $("#btn-newQuote").on("click", function() {
    var req = new XMLHttpRequest();
    req.open("POST", apiURL,true);
    req.setRequestHeader("X-Mashape-Key","pyRPRPd8mTmshfHzO0DmZyZdoejbp1uUdz3jsnfkDZXZJkYesX");
    req.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    req.setRequestHeader("Accept","application/json");
    req.responseType = "json";
    req.onload = function() {
      if (req.status === 200) {
        quote = req.response;
      } 
      else {
        console.log("req.status = " + req.status);
      }
    }
    req.send();
    if(quote.quote !== undefined) {
      $("#quoteText").html(quote.quote)
      $("#quoteAuthor").html("- <b>" + quote.author + "</b>")
      $("#quoteText").animateCss("fadeIn");
      $("#quoteAuthor").animateCss("fadeIn");
      var tweetURL = "https://twitter.com/intent/tweet?text="+quote.quote+" ("+quote.author+")";
      console.log(tweetURL);
      $("#tweetButton").attr("disabled",false);
      $("#tweetLink").attr("href",tweetURL);
    }
  });
});