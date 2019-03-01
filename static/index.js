// Validate Login Credentials
markers=[];
sellers=[];
let info = new google.maps.InfoWindow();
$(document).ready(function()
{

    $(".clickable-row").click(function() {
        window.location = $(this).data('url');
    });


// Show info window at marker with content
function showInfo(marker, content)
{
    // Start div
    let div = "<div id='info'>";
    if (typeof(content) == "undefined")
    {
        // http://www.ajaxload.info/
        div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
    }
    else
    {
        div += content;
    }

    // End div
    div += "</div>";

    // Set info window's content
    info.setContent(div);

    // Open info window (if not already open)
    info.open(map, marker);
}


// Add marker for place to map
function addMarker(place)
{

    var myLatLng = {lat : place.latitude, lng : place.longitude};
    marker = new google.maps.Marker({
        position : myLatLng,
        map : map,
        title : place.shop_name
    });

    markers.push(marker);
    sellers.push(place.seller_phone);

    google.maps.event.addListener(marker,'click', function(event){

            for (var k = 0; k < markers.length; ++k)
            {
                if(markers[k].position.lat() == event.latLng.lat() && markers[k].position.lng() == event.latLng.lng())
                {
                    /*console.log(markers[k].getPosition().lat(),markers[k].getPosition().lng());  */
                    let q = {seller_phone : sellers[k]};
                    $.getJSON("/map_info",q, (function(data){
                        content_str = "<div class='p-1 mb-1 bg-secondary text-white' style='font-size:150%'>" + markers[k].getTitle() + "</div>";
                        content_str += "<ul>";
                        for (var i in data)
                        {
                            content_str += "<li>";
                            content_str += "<a href=" + "/product?product_id=" + data[i].product_id + ">"  + "<span class='text-md-left'>" + data[i].product_name + "</span>&nbsp &nbsp Rs." + "<span class='text-md-right'>" + data[i].price + "</span></a>";
                            content_str += "</li>";


                        }
                        content_str += "</ul>";
                        showInfo(markers[k],content_str);

                    }));
                break;
                }
            }

        });

}
function removeMarkers()
{
    for (var i = 0; i < markers.length; i++)
    {
        markers[i].setMap(null);
    }
    markers=[];
    sellers=[];
}
// Update UI's markers
function update()
{
    google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
    // Get map's bounds
    let bounds = map.getBounds();
    let ne = bounds.getNorthEast();
    let sw = bounds.getSouthWest();

    // Get places within bounds (asynchronously)
    let parameters = {
        ne: `${ne.lat()},${ne.lng()}`,
        sw: `${sw.lat()},${sw.lng()}`
    };
    $.getJSON("/update", parameters, function(data, textStatus, jqXHR) {

       // Remove old markers from map
       removeMarkers();

       // Add new markers to map
       for (let i = 0; i < data.length; i++)
       {
           addMarker(data[i]);
       }
    });
});}


    var map;




    infoWindow = new google.maps.InfoWindow;
    $.getJSON("/user_location", function(data, textStatus, jqXHR) {
    var pos = {
          lat: parseFloat(data.latitude),
          lng: parseFloat(data.longitude)
        };
        map = new google.maps.Map(document.getElementById('map-canvas'), {
       center: pos,
       zoom: 16
    });
        map.setCenter(pos);
        update();
    });




     // Update UI after zoom level changes
    google.maps.event.addListener(map, "zoom_changed", function() {
        update();
    });

}
);






