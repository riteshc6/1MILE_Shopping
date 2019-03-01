// Javascript to Validate form inputs on the client side

$(document).ready(function()
{
    // Show Delivery time Input Once delivery option selected.
    $("#yes").click(function(){
        $("#delivery_time").show();

    });

    $("#p_form").submit(function(){

        if (!$("#p_form input[name=product_name]").val())
        {
            alert("Missing Product_name");
            return false;
        }


        if(!$("#p_form input[name=brand]").val())
        {
            alert("Missing Brand name");
            return false;
        }

        if(!$("#p_form input[name=image]").val())
        {
            alert("Upload Image");
            return false;
        }

        if(!$("#p_form input[name=description]").val())
        {
            alert("Missing description");
            return false;
        }

        if(!$("#p_form input[name=stock]").val())
        {
            alert("Missing stock (Quantity of Item)");
            return false;
        }

        if(!$("#p_form input[name=mrp]").val())
        {
            alert("Select MRP");
            return false;
        }

        if(!$("#p_form input[name=price]").val())
        {
            alert("Missing Price");
            return false;
        }


        if ($('input[name=order_pick]:checked').length == 0) {
            alert("Missing order_pick");
            return false;
        }

        if($("input[name=delivery]:checked").length == 0)
        {
            alert("Missing Delivery option");
            return false;
        }

        else if($('#yes').is(':checked'))
        {
            // Ensures delivery_time is not empty
            if(!$("#p_form input[name=delivery_time]").val())
            {
                alert("Missing Delivery Time");
                return false;
            }

        }


        return true;
    });});
