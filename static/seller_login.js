// Validting Seller Login Credentials

$(document).ready(function(){
  $("#s_form").submit(function(){

      if(!$("#s_form input[name=seller_phone]").val())
      {
          alert("Must Provide Your Phone Number");
          return false;
      }

      if(!$("#s_form input[name=password]").val())
      {
          alert("Must Provide Your Password");
          return false;
      }
  }
  );
}
);