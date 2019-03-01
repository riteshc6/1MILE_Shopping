import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path
from geopy.distance import geodesic
from operator import itemgetter

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

from helpers import apology, user_login_required, seller_login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")

@app.route("/")
@user_login_required
def index():

    rows=db.execute("SELECT * FROM sellers")
    distance=[]
    user_location = (session["latitude"],session["longitude"])

    for row in rows:
        seller_location = (row["latitude"],row["longitude"])
        row["distance"] = round(geodesic(user_location, seller_location).km,2)
    newlist = sorted(rows, key=itemgetter('distance'))

    return render_template("index.html",rows=newlist,user_location=user_location)

    """If Not Logged in : Show Shops in Locality
                           BUY & SELL Options
                           Search Option for deifferent Locality
        ELSE : Show User.html or Seller.html  """
   # return apology("TODO")




@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    """ Register User """

    # User reached via POST(form submitted) or GET(render form)
    if request.method == "POST" :

        h = generate_password_hash(request.form.get("password"))
        row_id = db.execute("INSERT INTO users(user_name,user_phone,street_name,city,state,pin,email,password,latitude,longitude) VALUES(:user_name,:user_phone,:street_name,:city,:state,:pin,:email,:password,:latitude,:longitude)",
                                                user_name=request.form.get("user_name"), user_phone=request.form.get("user_phone"),street_name=request.form.get("street_name"),city=request.form.get("city"),state=request.form.get("state"),pin=request.form.get("pin"),email=request.form.get("email"),password=h,latitude=request.form.get("latitude"),longitude=request.form.get("longitude"))


        return render_template("confirm.html",user_phone=request.form.get("phone"))

    else :
        return render_template("user_register.html")

# Display User Profile
@app.route("/user_profile", methods=["GET","POST"])
@user_login_required
def user_profile():
    if request.method=="POST":
        db.execute("UPDATE users SET user_name=:user_name,user_phone=:user_phone,latitude=:latitude,longitude=:longitude,street_name=:street_name,city=:city,state=:state,pin=:pin,state=:state,email=:email WHERE user_phone=:user_phone",
                                    user_name=request.form.get("user_name"),latitude=request.form.get("latitude"),longitude=request.form.get("longitude"),street_name=request.form.get("street_name"),city=request.form.get("city"),state=request.form.get("state"),pin=request.form.get("pin"),email=request.form.get("email"),user_phone=session.get("user_phone"))
        flash("Your Profile has been Successfully Updated")
        return redirect("/user_profile")

    else:
        row = db.execute("SELECT * FROM users WHERE user_phone=:user_phone", user_phone=session.get("user_phone"))
        return render_template("user_profile.html",row=row)





@app.route("/user_password", methods=["GET","POST"])
@user_login_required
def user_password():
    if request.method == "POST":

        row = db.execute("SELECT * FROM users WHERE user_phone = :user_phone", user_phone=session.get("user_phone"))
        if check_password_hash(row[0]["password"], request.form.get("password")):
            h = generate_password_hash(request.form.get("n_password"))
            db.execute("UPDATE users set password = :h WHERE user_phone = :user_phone", h=h, user_phone=session.get("user_phone"))
            flash("Your Password has been successfully changed")
            return redirect("/")
        else:
            return apology("Enter correct current password")

    else:
        return render_template("user_password.html")


@app.route("/shop")
@user_login_required
def shop(**seller_phone):

    rows = db.execute("SELECT * FROM products WHERE seller_phone = :seller_phone",seller_phone=request.args.get('seller_phone'))
    return render_template("shop.html",rows=rows,shop_name=request.args.get("shop_name"))

@app.route("/map_info")
@user_login_required
def map_info():
    rows = db.execute("SELECT * FROM products WHERE seller_phone = :seller_phone",seller_phone=request.args.get('seller_phone'))
    print(rows)
    return jsonify(rows)




@app.route("/product")
@user_login_required
def product(**product_id):
    product_id=request.args.get("product_id")
    row = db.execute("SELECT * FROM products WHERE product_id=:product_id",product_id=product_id)
    return render_template("product.html",row=row)


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE user_phone=:user_phone",
                          user_phone=request.form.get("user_phone"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_phone"] = rows[0]["user_phone"]

        # Remember Geo Coordinates to find the nearest shops
        session["latitude"] = rows[0]["latitude"]
        session["longitude"] = rows[0]["longitude"]

        # Redirect user to home page
        return redirect("/")

    else :
        return render_template("user_login.html")


@app.route("/user_orders")
@user_login_required
def user_orders(**product_id):
    """ Update the order_history database and display user's order history"""
    if request.args.get("product_id"):
        row=db.execute("SELECT * FROM products WHERE product_id=:product_id",product_id=request.args.get("product_id"))
        db.execute("INSERT INTO order_history(product_id,product_name,user_phone,seller_phone,price,order_type,status) VALUES(:product_id,:product_name,:user_phone,:seller_phone,:price,:order_type,:status)",
                    product_id=row[0]['product_id'],product_name=row[0]['product_name'],user_phone=session.get('user_phone'),seller_phone=row[0]['seller_phone'], price=row[0]['price'],order_type=request.args.get("order_type"),status="pending")
        flash("Your Order has been Executed")
        return redirect("/")

    else :
        rows=db.execute("SELECT * FROM order_history WHERE user_phone=:user_phone",user_phone=session.get("user_phone"))
        shop_name=[]
        for row in rows:
            shop_name = shop_name + db.execute("SELECT shop_name FROM sellers WHERE seller_phone=:seller_phone",seller_phone=row['seller_phone'])
        return render_template("user_orders.html",rows=rows,shop_name=shop_name)



@app.route("/logout")
def logout():
    """Log user out"""
    if session.get("user_phone"):
        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")
    else:
        session.clear()
        return redirect("/seller_login")



@app.route("/seller_register", methods=["GET", "POST"])
def seller_register():
      """ Register User """

    # User reached via POST(form submitted) or GET(render form)
      if request.method=="POST":

        UPLOAD_FOLDER = 'static/shop_images'
        ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
        basedir = os.path.abspath(os.path.dirname(__file__))


        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        def allowed_file(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        h = generate_password_hash(request.form.get("password"))
        row_id = db.execute("INSERT INTO sellers(shop_name,seller_name,seller_phone,street_name,city,state,pin,email,password,latitude,longitude) VALUES(:shop_name, :seller_name,:seller_phone,:street_name,:city,:state,:pin,:email,:password,:latitude,:longitude)",
                            shop_name=request.form.get("shop_name"), seller_name=request.form.get("seller_name"), seller_phone=request.form.get("seller_phone"),street_name=request.form.get("street_name"),city=request.form.get("city"),state=request.form.get("state"),pin=request.form.get("pin"),email=request.form.get("email"),password=h,latitude=request.form.get("latitude"),longitude=request.form.get("longitude"))

             # Store the file name as product_id.suffix in images folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            suffix = os.path.splitext(filename)[1]
            filename = str(request.form.get("seller_phone")) + suffix    # suffix is added to preserve the orginal file format
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

        # Update the image file name using 'filename'
        db.execute("UPDATE sellers SET image=:filename WHERE seller_phone=:seller_phone",filename=filename,seller_phone=request.form.get("seller_phone"))
        flash("You are Registered Now")

        return render_template("confirm.html",seller_phone=request.args.get("seller_phone"))

      else:
          return render_template("seller_register.html")


@app.route("/add_product", methods=["GET", "POST"])
@seller_login_required
def add_product():
    """Show a detailed view of product and options to buy product"""
    if request.method == "POST":

        product_name = request.form.get("product_name")


        seller_phone = session.get("seller_phone")

        brand = request.form.get("brand")

        image = request.form.get("image")


        description = request.form.get("description")

        stock=request.form.get("stock")

        mrp = request.form.get("mrp")

        price = request.form.get("price")

        order_pick = request.form.get("order_pick")

        delivery = request.form.get("delivery")

        delivery_time = request.form.get("delivery_time")

        UPLOAD_FOLDER = 'static/product_images'
        ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(os.path.dirname(__file__))

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        def allowed_file(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            # row_id=product_id which is a ineteger primary key autogenerated by database
            row_id = db.execute("INSERT INTO products(seller_phone,product_name,brand,description,mrp,price,stock,order_pick,delivery,delivery_time) VALUES(:seller_phone,:product_name,:brand,:description,:mrp, :price, :stock,:order_pick,:delivery, :delivery_time)",
                                                     seller_phone=seller_phone,product_name=product_name, brand=brand, description=description, mrp=mrp, price=price, stock=stock, order_pick=order_pick, delivery=delivery, delivery_time=delivery_time)

        # Store the file name as product_id.suffix in images folder

            filename = secure_filename(file.filename)
            suffix = os.path.splitext(filename)[1]
            filename = str(row_id) + suffix    # suffix is added to preserve the orginal file format
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        else :
            flash("Invalid File Type, Try .jpg, .png, .jpeg")
            return redirect("/add_product")
        # Update the image file name using 'filename'
        db.execute("UPDATE products SET image=:filename WHERE rowid= :row_id",filename=filename,row_id=row_id)
        flash("Your Product has been added to your Inventory")
        return redirect("/inventory")

    else:
        return render_template("add_product.html")




@app.route("/history")
@seller_login_required
def history():
    rows=db.execute("SELECT * FROM order_history WHERE seller_phone=:seller_phone",seller_phone=session.get("seller_phone"))
    users=[]
    for row in rows:
            users = users + db.execute("SELECT street_name,pin,user_name FROM users WHERE user_phone=:user_phone",user_phone=row['user_phone'])

    return render_template("seller_orders.html",rows=rows,users=users)

@app.route("/accept_order", methods=["GET","POST"])
@seller_login_required
def accept_order():
    if request.method == "POST":
        order_id=request.args.get("order_id")
        delivery_time = request.form.get("delivery_time")
        row=db.execute("UPDATE order_history SET status=:status,delivery_time=:delivery_time WHERE order_id=:order_id",status="accepted",delivery_time=delivery_time, order_id=order_id)
        db.execute("UPDATE products SET stock = (stock - 1) WHERE product_id=:product_id",product_id=request.args.get("product_id"))
        flash("You have Successfully accepted the Order")
        return redirect("/seller_index")

    else:
        users=db.execute("SELECT * FROM users WHERE user_phone=:user_phone",user_phone=request.args.get("user_phone"))
        row=db.execute("SELECT * FROM products WHERE product_id=:product_id",product_id=request.args.get("product_id"))
        return render_template("reply.html",order_type=request.args.get("order_type"),order_id=request.args.get("order_id"),row=row,users=users)


@app.route("/seller_index")
@seller_login_required
def seller_index():
    rows=db.execute("SELECT * FROM order_history WHERE seller_phone=:seller_phone AND status=:status",seller_phone=session.get("seller_phone"),status="pending")
    users=[]
    for row in rows:
            users = users + db.execute("SELECT street_name,pin,user_name FROM users WHERE user_phone=:user_phone",user_phone=row['user_phone'])

    return render_template("seller_index.html",rows=rows,users=users)


@app.route("/seller_profile", methods=["GET","POST"])
@seller_login_required
def seller_profile():
    if request.method=="POST":
        db.execute("UPDATE sellers SET shop_name=:shop_name,seller_name=:seller_name,seller_phone=:seller_phone,latitude=:latitude,longitude=:longitude,street_name=:street_name,city=:city,state=:state,pin=:pin,state=:state,email=:email WHERE seller_phone=:seller_phone",
                                    shop_name=request.form.get("shop_name"),seller_name=request.form.get("seller_name"),latitude=request.form.get("latitude"),longitude=request.form.get("longitude"),street_name=request.form.get("street_name"),city=request.form.get("city"),state=request.form.get("state"),pin=request.form.get("pin"),email=request.form.get("email"),seller_phone=session.get("seller_phone"))
        flash("Your Profile has been Successfully Updated")
        return redirect("/seller_profile")

    else:
        row = db.execute("SELECT * FROM sellers WHERE seller_phone=:seller_phone", seller_phone=session.get("seller_phone"))
        return render_template("seller_profile.html",row=row)


@app.route("/seller_password", methods=["GET","POST"])
@seller_login_required
def seller_password():
    if request.method == "POST":

        row = db.execute("SELECT * FROM sellers WHERE seller_phone = :seller_phone", seller_phone=session.get("seller_phone"))
        if check_password_hash(row[0]["password"], request.form.get("password")):
            h = generate_password_hash(request.form.get("n_password"))
            db.execute("UPDATE sellers set password = :h WHERE seller_phone = :seller_phone", h=h, seller_phone=session.get("seller_phone"))
            flash("Your Password has been successfully changed")
            return redirect("/seller_index")
        else:
            return apology("Enter correct current password")

    else:
        return render_template("seller_password.html")


@app.route("/inventory")
@seller_login_required
def inventory():
    rows=db.execute("SELECT * FROM products WHERE seller_phone=:seller_phone",seller_phone=session.get("seller_phone"))
    return render_template("inventory.html",rows=rows)

@app.route("/edit_product", methods=["GET","POST"])
@seller_login_required
def edit_product():
    if request.method=="POST":
        print("post")
        db.execute("UPDATE products SET product_name=:product_name,brand=:brand,description=:description,stock=:stock,mrp=:mrp,price=:price,order_pick=:order_pick,delivery=:delivery,delivery_time=:delivery_time WHERE product_id=:product_id",
                                        product_name=request.form.get("product_name"),brand=request.form.get("brand"),description=request.form.get("description"),stock=request.form.get("stock"),mrp=request.form.get("mrp"),price=request.form.get("price"),order_pick=request.form.get("order_pick"),delivery=request.form.get("delivery"),delivery_time=request.form.get("delivery_time"),product_id=request.args.get("product_id"))
        flash("Your Product has been succesfully Updated")
        return redirect("/inventory")

    else:
        print("get")
        row=db.execute("SELECT * FROM products WHERE product_id=:product_id",product_id=request.args.get("product_id"))
        return render_template("edit_product.html",row=row)


@app.route("/delete")
@seller_login_required
def delete():
    file_path="product_images/" + request.args.get("image")
    file_handle = open(os.path.join(app.static_folder, file_path), 'r')
    os.remove(os.path.join(app.static_folder, file_path))
    file_handle.close()
    db.execute("DELETE FROM products WHERE product_id=:product_id",product_id=request.args.get("product_id"))

    flash("Your Product has been deleted")
    return redirect("/inventory")


@app.route("/seller_login", methods=["GET", "POST"])
def seller_login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM sellers WHERE seller_phone = :seller_phone",
                          seller_phone=request.form.get("seller_phone"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["seller_phone"] = rows[0]["seller_phone"]

        # Redirect user to home page
        return redirect("/seller_index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("seller_login.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM sellers
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM fts_places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)