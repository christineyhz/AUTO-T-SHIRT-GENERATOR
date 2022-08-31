from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField, validators
from werkzeug.utils import secure_filename
import os
from os.path import isfile, join
from wtforms.validators import InputRequired
from algorithm.trend import get_image_url
from algorithm.etsy_scrape import get_sales_info
from algorithm.base64tohtml import base64toimg
from algorithm.ebay_image_search import get_ebay_info
BASEDIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASEDIR, 'static/files')

app = Flask(__name__)

key = os.urandom(24)

app.secret_key = key
app.config['SECRET_KEY'] = key
app.config['UPLOAD_FOLDER'] = 'static/files'

# This ensures the files folder is always empty when the application is launched
for f in os.listdir(STATIC_DIR):
    os.remove(os.path.join(STATIC_DIR, f))

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired(),FileAllowed(['jpg','png'])]) # file should not be empty and only images can be uploaded
    title = StringField("Title", [validators.DataRequired(), validators.Length(min=1,max=100,message="Title too long, the max is 100 characters")])
    submit = SubmitField("Upload File")

class Item:
        def __init__(self, vals):
            self.__dict__ = vals


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/design',methods = ["GET","POST"])
def design():
    if request.method == 'GET':
        search_term = request
        return render_template('design.html')
    
    else:
        search_term = request.form['search_term']
        session['search_term'] = search_term
        print(search_term)
        print('Start searching images...')
        imagelist, trend_words, formated_search_term = get_image_url(search_term)
        try:
            image_first_shown_src = imagelist[0]['image_link']
            image_first_shown_alt = imagelist[0]['name']
            session['trend_words'] = trend_words
            session['image_first_shown_src'] = image_first_shown_src
            session['image_first_shown_alt'] = image_first_shown_alt
            session['formated_search_term'] = formated_search_term
            session['imagelist'] = imagelist
            session ['show'] = 'valid'
            print(trend_words)
            print(image_first_shown_src)
            print(image_first_shown_alt)
            print(formated_search_term)
            print(imagelist)
        except:
            pass

        return render_template ('design_with_an_idea.html', search_term = search_term, formated_search_term = formated_search_term, trend_words = trend_words, image_first_shown_src = image_first_shown_src, image_first_shown_alt = image_first_shown_alt, images = [Item(i) for i in imagelist])
       

@app.route('/design-with-an-idea-hide',methods = ["POST"])
def design_with_idea():
    try:    
        # receiving json data
        data = request.get_json(force=True)
        print('Saved data received...')
        image_title = data['name']
        base64 = data['base'] # This is the saved T-Shirt design image, which is used to be searched in eBay API, and writing to the base_saved_design.html
        base64_pure = base64.replace('data:image/png;base64,', '') # This stripes the prefix of the base64 and can be used in eBay image search

        # Writing the image tag in base_saved_design.html
        print('Writing the saved image base file...')
        base64toimg(base64)
        productlist_ebay = get_ebay_info(base64_pure)

        design_name = image_title +  " " + session['formated_search_term'] + " T-Shirt"
        session['design_name'] = design_name
        session['productlist'] = productlist_ebay
        session['analyse'] = 1
        print('done!!')

    except:
        pass
    
    return render_template ('home.html')
        

    
@app.route('/design-with-an-image-upload', methods=['GET',"POST"])
def upload_image():

    form = UploadFileForm()

    if form.validate_on_submit():
        # clearing the files folder to make sure previous uploaded file is removed
        if 'uploaded' in session:
            if session['uploaded'] == 1:
                 for f in os.listdir('./static/files'):
                    os.remove(os.path.join('./static/files', f))
                    session['uploaded'] = 0


        file = form.file.data # First grab the file
        title = form.title
       
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        session['uploaded'] = 1
        files = [f for f in os.listdir('./static/files') if isfile(join('./static/files', f))]

        filename = files[0]
        img_alt = title.data
        img_src = '../static/files/' + filename
    
        return render_template('design_with_an_image.html', img_src = img_src, img_alt = img_alt)
    
    return render_template('design_with_image_upload.html', form=form)


@app.route('/design-with-an-image-hide',methods = ["POST"])
def design_with_image():
    try:    
        # receiving json data
        data = request.get_json(force=True)
        print('Saved data received...')
        image_title = data['name']
        base64 = data['base'] # This is the saved T-Shirt design image, which is used to be searched in eBay API, and writing to the base_saved_design.html
        base64_pure = base64.replace('data:image/png;base64,', '') # This stripes the prefix of the base64 and can be used in eBay image search

        # Writing the image tag in base_saved_design.html
        print('Writing the saved image base file...')
        base64toimg(base64)
        productlist_ebay = get_ebay_info(base64_pure)

        design_name = image_title + " T-Shirt"
        session['design_name'] = design_name
        session['productlist'] = productlist_ebay
        session['analyse'] = 2
        print('done!!')

    except:
        pass
    
    return render_template ('home.html')



@app.route('/analysis-with-an-idea')
def analysis_idea():
    if 'analyse' in session:
        if session['analyse'] == 1:
            productlist = session ['productlist']
            design_name = session ['design_name']
            print('the design name is:')
            print(design_name)
            print('start searching on Etsy...')
            avg_sale, product_container_etsy = get_sales_info(design_name)
            print(product_container_etsy)
            print('Done with Etsy')
            session['analyse'] = 0

            return render_template('analysis.html',  design_name = design_name , products = [Item(i) for i in productlist] , avg_sale = avg_sale, etsy = [Item(i) for i in product_container_etsy])
        
        else:
            return redirect(url_for('home'))
       
    else: # if the user attempt to enter this page directly, redirect the user to the design page
        return redirect(url_for('home'))


@app.route('/analysis-with-an-image')
def analysis_image():
    if 'analyse' in session:
        if session['analyse'] == 2:
            productlist = session ['productlist']
            design_name = session ['design_name']
            print('the design name is:')
            print(design_name)
            print('start searching on Etsy...')
            avg_sale, product_container_etsy = get_sales_info(design_name)
            print(product_container_etsy)
            print('Done with Etsy')
            session['analyse'] = 0

            return render_template('analysis.html',  design_name = design_name , products = [Item(i) for i in productlist] , avg_sale = avg_sale, etsy = [Item(i) for i in product_container_etsy])
        
        else:
            return redirect(url_for('home'))

    else: # if the user attempt to enter this page directly, redirect the user to the design page
        return redirect(url_for('home'))


@app.route('/Instruction')
def instruction():
    return render_template('instruction.html')


@app.route('/About')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')

@app.errorhandler(405)
def error_405(error):
    return render_template('405.html')


if __name__ == '__main__':
    app.run(debug=True)
