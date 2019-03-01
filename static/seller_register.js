// Javascript to Validate form inputs on the client side

$(document).ready(function()
{
    var map;





infoWindow = new google.maps.InfoWindow;

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            map = new google.maps.Map(document.getElementById('map'), {
             center: pos,
            zoom: 18
            });
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

    $("#sr_form").submit(function()
    {

        if (!$("#sr_form input[name=shop_name]").val())
        {
            alert("Missing Shop_name");
            return false;
        }

        else if(!$("#sr_form input[name=seller_name]").val())
        {
            alert("Missing Seller Name");
            return false;
        }

        else if(!$("#sr_form input[name=seller_phone]").val())
        {
            alert("Missing Phone Number");
            return false;
        }

        if(!$("#sr_form input[name=image]").val())
        {
            alert("Upload Image");
            return false;
        }

        else if(!$("#sr_form input[name=street_name]").val())
        {
            alert("Missing Street name");
            return false;
        }

        else if(!$("#sr_form input[name=city]").val())
        {
            alert("Missing City Name");
            return false;
        }

        else if(!$("#state option:selected").val())
        {
            alert("Select State");
            return false;
        }

        else if(!$("#sr_form input[name=pin]").val())
        {
            alert("Missing Pin Code");
            return false;
        }

        else if(!$("#sr_form input[name=email]").val())
        {
            alert("Missing Email");
            return false;
        }


        else if(!$("#sr_form input[name=password]").val())
        {
            alert("Missing Password");
            return false;
        }

        else if($("#sr_form input[name=password]").val() != $("#sr_form input[name=confirm_password]").val())
        {
            alert("Passwords don't Match");
            return false;
        }

        return true;
    });});
