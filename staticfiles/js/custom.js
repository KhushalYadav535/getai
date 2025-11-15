$(document).ready(function () {
  $(".sidebar_toggler").click(function () {
      $("#sidebar").toggleClass("show");
      $("#flowBody").toggleClass("overFlow_hide");
  });


  $(".fltBtn").click(function () {
    $(".el-checkbox").toggleClass("is-checked");
    $(".el-checkbox__input").toggleClass("is-checked");
});


$(".scroll-top").click(function() {
  $("html, body").animate({
      scrollTop: 0
  }, "fast");
  return false;
});

  var langArray = [];
    $('.vodiapicker option').each(function(){
      var img = $(this).attr("data-thumbnail");
      var text = this.innerText;
      var value = $(this).val();
      var item = '<li><img src="'+ img +'" alt="" value="'+value+'"/><span>'+ text +'</span></li>';
      langArray.push(item);
    })
    
    $('#a').html(langArray);
    
    //Set the button value to the first el of the array
    $('.btn-select').html(langArray[0]);
    $('.btn-select').attr('value', 'en');
    
    //change button stuff on click
    $('#a li').click(function(){
       var img = $(this).find('img').attr("src");
       var value = $(this).find('img').attr('value');
       var text = this.innerText;
       var item = '<li><img src="'+ img +'" alt="" /><span>'+ text +'</span></li>';
      $('.btn-select').html(item);
      $('.btn-select').attr('value', value);
      $(".b").toggle();
      //console.log(value);
    });
    
    $(".btn-select").click(function(){
            $(".b").toggle();
        });
    
    //check local storage for the lang
    var sessionLang = localStorage.getItem('lang');
    if (sessionLang){
      //find an item with value of sessionLang
      var langIndex = langArray.indexOf(sessionLang);
      $('.btn-select').html(langArray[langIndex]);
      $('.btn-select').attr('value', sessionLang);
    } else {
       var langIndex = langArray.indexOf('ch');
      console.log(langIndex);
      $('.btn-select').html(langArray[langIndex]);
      //$('.btn-select').attr('value', 'en');
    }



    var marker = $('#marker'),
  current = $('.current');

// Initialize the marker position and the active class
current.addClass('active');
marker.css({
  // Place the marker in the middle of the border
  bottom: -(marker.height() / 2),
  left: current.position().left,
  width: current.outerWidth(),
  display: "block"
});


if (Modernizr.csstransitions) {
console.log("using css3 transitions");
$('.nav-item').mouseover(function () {
  var self = $(this),
      offsetLeft = self.position().left,
      // Use the element under the pointer OR the current page item
      width = self.outerWidth() || current.outerWidth(),
      // Ternary operator, because if using OR when offsetLeft is 0, it is considered a falsy value, thus causing a bug for the first element.
      left = offsetLeft == 0 ? 0 : offsetLeft || current.position().left;
// Play with the active class
  $('.active').removeClass('active');
  self.addClass('active');
  marker.css({
      left: left,
      width: width,
  });
});

// When the mouse leaves the menu
$('#ul').mouseleave(function () {
// remove all active classes, add active class to the current page item
  $('.active').removeClass('active');
  current.addClass('active');
// reset the marker to the current page item position and width
  marker.css({
      left: current.position().left,
      width: current.outerWidth()
  });
});

} else {
console.log("using jquery animate");

$('.nav-item').mouseover(function () {
  var self = $(this),
      offsetLeft = self.position().left,
      // Use the element under the pointer OR the current page item
      width = self.outerWidth() || current.outerWidth(),
      // Ternary operator, because if using OR when offsetLeft is 0, it is considered a falsy value, thus causing a bug for the first element.
      left = offsetLeft == 0 ? 0 : offsetLeft || current.position().left;
// Play with the active class
  $('.active').removeClass('active');
  self.addClass('active');
  marker.stop().animate({
      left: left,
      width: width,
  }, 300);
});

// When the mouse leaves the menu
$('#ul').mouseleave(function () {
// remove all active classes, add active class to the current page item
  $('.active').removeClass('active');
  current.addClass('active');
// reset the marker to the current page item position and width
  marker.stop().animate({
      left: current.position().left,
      width: current.outerWidth()
  }, 300);
});
};
});




// Scroll handler - ensure jQuery is loaded
$(document).ready(function() {
    $(document).scroll(function() {
        var y = $(this).scrollTop();
        if (y > 200) {
            // Check if fadeIn exists (jQuery Slim doesn't have it)
            if (typeof $.fn.fadeIn === 'function') {
                $('.scroll-top').fadeIn();
            } else {
                $('.scroll-top').show();
            }
        } else {
            // Check if fadeOut exists (jQuery Slim doesn't have it)
            if (typeof $.fn.fadeOut === 'function') {
                $('.scroll-top').fadeOut();
            } else {
                $('.scroll-top').hide();
            }
        }
    });
});



const typedTextSpan = document.querySelector(".typed-text");
const cursorSpan = document.querySelector(".cursor");

// Only initialize typing animation if elements exist
if (typedTextSpan && cursorSpan) {
  const textArray = ["Tool", "News", "Research"];
  const typingDelay = 200;
  const erasingDelay = 100;
  const newTextDelay = 2000; // Delay between current and next text
  let textArrayIndex = 0;
  let charIndex = 0;

  function type() {
    if (charIndex < textArray[textArrayIndex].length) {
      if(!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing");
      typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
      charIndex++;
      setTimeout(type, typingDelay);
    } 
    else {
      cursorSpan.classList.remove("typing");
      setTimeout(erase, newTextDelay);
    }
  }

  function erase() {
    if (charIndex > 0) {
      if(!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing");
      typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex-1);
      charIndex--;
      setTimeout(erase, erasingDelay);
    } 
    else {
      cursorSpan.classList.remove("typing");
      textArrayIndex++;
      if(textArrayIndex>=textArray.length) textArrayIndex=0;
      setTimeout(type, typingDelay + 1100);
    }
  }

  document.addEventListener("DOMContentLoaded", function() { // On DOM Load initiate the effect
    if(textArray.length) setTimeout(type, newTextDelay + 250);
  });
}