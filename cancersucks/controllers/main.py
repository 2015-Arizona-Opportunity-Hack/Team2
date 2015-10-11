from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, make_response, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user

from cancersucks.extensions import cache
from cancersucks.forms import LoginForm
from cancersucks.models import User, db, Message, Meetup
from flask.ext.admin import Admin
from flask.ext.admin.contrib import sqla
from functools import update_wrapper
from datetime import timedelta
from sqlalchemy import or_
admin = Admin()
class MyModelView(sqla.ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    def is_accessible(self):
        return current_user.is_authenticated()

    def _handle_view(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        if not self.is_accessible():
            return redirect("/login")


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Message, db.session))
admin.add_view(MyModelView(Meetup, db.session))
main = Blueprint('main', __name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@main.route('/')
@login_required
@cache.cached(timeout=1000)
def home():
    all_users = User.query.all()
    markers = []
    for elem in all_users:
        temp = [str(elem.username), str(elem.longlat).split(",")[0], str(elem.longlat).split(",")[-1]]         
        markers.append(temp)
    return render_template('maps.html', lats=markers)


@main.route("/login", methods=["GET", "POST"])
def login():
    #form = LoginForm()
    if request.method=="POST":
    #if form.validate_on_submit():
        user = User.query.filter_by(username=request.form.get('username')).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("signin.html")
@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method=="POST":
        username = request.form.get('username') if request.form.get('username') else ""
        firstname = request.form.get('firstname') if request.form.get('firstname') else ""
        lastname = request.form.get('lastname') if request.form.get('lastname') else ""
        password = request.form.get('password') if request.form.get('passowrd') else ""
        email = request.form.get('email') if request.form.get('email') else ""
        newuser = User(username=username, password=password, email=email, firstname=firstname, lastname=lastname)
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        return render_template("acctype.html")

    return render_template("signup.html")
@main.route("/approve/<acc_type>", methods=["GET", "POST"])
def approove(acc_type):
    if request.method=="POST":
        address = request.form.get('address') if request.form.get('address') else ""
        phonenum = request.form.get('phonenum') if request.form.get('phonenum') else ""
        treat_cen = request.form.get('treatcen') if request.form.get('treatcen') else ""
        child_name = request.form.get('childname') if request.form.get('childname') else ""
        child_dob = request.form.get('childdob') if request.form.get('childdob') else ""
        child_hobbies = request.form.get('childhob') if request.form.get('childhob') else ""
        longlat = request.form.get('longlat') if request.form.get('longlat') else ""
        social_name = request.form.get('socialname') if request.form.get('socialname') else ""
        social_num = request.form.get('socialnum') if request.form.get('socialnum') else ""
        dob = request.form.get('dob') if request.form.get('dob') else ""
        facebook = request.form.get('facebook') if request.form.get('facebook') else ""
        twitter = request.form.get('twitter') if request.form.get('twitter') else ""
        state = request.form.get('state') if request.form.get('state') else ""
        diagnosis = request.form.get('diagnosis') if request.form.get('diagnosis') else ""
        acc_type = request.form.get('acctype') if request.form.get('acctype') else ""
        siblings= request.form.get('siblings') if request.form.get('siblings') else ""
        about_me = request.form.get('aboutme') if request.form.get('aboutme') else ""
        user = User.query.filter_by(id = current_user.id).first()        
        user.address=address
        user.phone_number=phonenum
        user.treatment_center=treat_cen
        user.children_name=child_name
        user.children_age=child_dob
        user.children_hobbies=child_hobbies
        user.longlat=longlat
        user.social_worker_name=social_name
        user.social_worker_phone=social_num
        user.birthday=dob
        user.facebook=facebook
        user.twitter=twitter
        user.state=state
        user.diagnosis=diagnosis
        user.acc_type = acc_type
        user.siblings=siblings
        db.session.add(user)
        db.session.commit()
        return render_template("msg.html", msg="Your application has been submitted, you will receive an email upon approval!")
    if acc_type=="personal":
        return render_template("approve1.html", acc_type="personal")
    else:
        return render_template("approve2.html", acc_type="parent")
   



@main.route("/message", methods=["GET", "POST"])
@login_required
def msgs():
    if request.method == "POST":
        msg = request.form.get('msg')
        receiver = request.form.get('receiver_email')
        sender = current_user.id 
        receiver_id = User.query.filter_by(email=receiver_email).first().id
        newmsg = Message(sender_id=sender, receiver_id = receiver_id, msg=msg)
        db.session.add(newmsg)
        db.session.commit()
        return jsonify({'success': True})
#    msgs = db.session.query(Message).filter(or_(Message.sender_id==current_user.id, Message.receiver_id==current_user.id)).order_by(Message.date)
#    msglist = {}
#    for elem in msgs:
#        tempid = elem.sender_id if elem.sender_id!=current_user.id else elem.receiver_id
#        if tempid in msglist:
#            msglist[tempid].append({elem.sender_id: [elem.msg, elem.date]})
#        else:
#            msglist[tempid] = []
#            msglist[tempid].append({elem.sender_id: [elem.msg, elem.date]})
    return render_template('message.html')        
        
       
@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))

@main.route("/markers", methods=["GET", 'OPTIONS'])
#@crossdomain(origin='*')
def markers():
    all_users = User.query.all()
    local_obj = []
    global_obj = []
    for elem in all_users:
        temp_obj = {}
        temp_obj["name"] = str(elem.firstname) +  " " + str(elem.lastname)
        temp_obj["email"] = elem.email
        temp_obj["state"] = elem.state
        temp_obj["username"] = elem.username
        temp_obj["acc_type"] = elem.acc_type
        temp_obj["lat"] = str(elem.longlat).split(",")[0]
        temp_obj["long"] = str(elem.longlat).split(",")[-1]
        temp_obj["diagnosis"] = elem.diagnosis
        temp_obj["treatment_center"] = elem.treatment_center
        temp_obj["children_name"] = elem.children_name
        temp_obj["children_age"] = elem.children_age
        temp_obj["children_hobbies"] = elem.children_hobbies
        try:
            current_user.state
        except:
             current_user.state = "AZ"
        if elem.state == current_user.state:
            local_obj.append(temp_obj)
        else:
            global_obj.append(temp_obj)
        
    json_reply = {}
    json_reply['local'] = local_obj
    json_reply['global'] = global_obj
    response = make_response(jsonify(json_reply) )         
    response.headers['Access-Control-Allow-Origin'] = "*" 
    return response
@main.route("/user/<username>", methods=["GET"])
@login_required
def userdata(username):
    elem = User.query.filter_by(username=username).one()
    temp_obj = {}
    temp_obj["name"] = str(elem.firstname) +  " " + str(elem.lastname)
    temp_obj["email"] = elem.email
    temp_obj["state"] = elem.state
    temp_obj["username"] = elem.username
    temp_obj["acc_type"] = elem.acc_type
    temp_obj["longlat"] = elem.longlat
    temp_obj["diagnosis"] = elem.diagnosis
    temp_obj["treatment_center"] = elem.treatment_center
    temp_obj["children_name"] = elem.children_name
    temp_obj["children_age"] = elem.children_age
    temp_obj["children_hobbies"] = elem.children_hobbies
    temp_obj["birthday"] = elem.birthday
    temp_obj["about_me"] = elem.about_me
    return jsonify(temp_obj) 
 
@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200
