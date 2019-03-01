// Javascript Jquerry to Validate form inputs on the client side
var map;

$(document).ready (function(){



map = new google.maps.Map(document.getElementById('map'), {
  center: {lat: 17.47929254863756, lng: 78.39185032579496},
  zoom: 2
});


infoWindow = new google.maps.InfoWindow;

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            var marker = new google.maps.Marker({
            position : {lat: pos.lat, lng: pos.lng},
            draggable : true,
            map : map
            });
            document.getElementById("latitude").setAttribute("value", pos.lat);
            document.getElementById("longitude").setAttribute("value",pos.lng);
            infoWindow.setPosition(pos);
            infoWindow.setContent('Your Location');
            infoWindow.open(map,marker);
            map.setCenter(pos);

            marker.addListener('dragend',function(){
            document.getElementById("latitude").setAttribute("value", marker.getPosition().lat());
            document.getElementById("longitude").setAttribute("value",marker.getPosition().lng());
                        infoWindow.setPosition(pos);
            infoWindow.setContent('Your Location');
            infoWindow.open(map,marker);
            map.setCenter(pos);
            });
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }


      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }




$('#register').submit(function()
{
    if (!$("#register input[name=user_name]").val())
    {
        alert("Missing User_name");
        return false;
    }

    else if(!$("#register input[name=user_phone]").val())
    {
        alert("Missing Phone Number");
        return false;
    }

    else if(!$("#register input[name=street_name]").val())
    {
        alert("Missing street_name");
        return false;
    }

    else if(!$("#register input[name=city]").val())
    {
        alert("Missing City Name");
        return false;
    }

    else if(!$("#state option:selected").val())
    {
        alert("Select State");
        return false;
    }

    else if(!$("#register input[name=pin]").val())
    {
        alert("Missing Pin Code");
        return false;
    }

    else if(!$("#register input[name=email]").val())
    {
        alert("Missing Email");
        return false;
    }

    else if(!$("#register input[name=password]").val())
    {
        alert("Missing Password");
        return false;
    }

    else if($("#register input[name=password]").val() != $("#register input[name=confirm_password]").val())
    {
        alert("Passwords don't Match");
        return false;
    }
    alert("Remember your Phone Number is your Login Id");
    return true;
}); });
