var map;

$(document).ready (function(){

  $("#s-edit").click(function(){
        $('input[type=text]').removeAttr('readonly');
        $('#state').attr('disabled',false);
        $("#s-edit").hide();
        $("#s-map-edit").show();
        $('#s-save').show();



map = new google.maps.Map(document.getElementById('s-map'), {
  center: {lat: 17.47929254863756, lng: 78.39185032579496},
  zoom: 14
});


infoWindow = new google.maps.InfoWindow;

// Try HTML5 geolocation.

var pos = {
  lat: parseFloat($("#s-profile input[name=latitude]").val()),
  lng: parseFloat($("#s-profile input[name=longitude]").val())
};
console.log(pos);
var marker = new google.maps.Marker({
position : {lat: pos.lat, lng: pos.lng},
draggable : true,
map : map
});
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



    });

});