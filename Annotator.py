import os
import json
from flask import Flask,render_template, flash, request, redirect, url_for, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
from analysePDF import processPDF
from modeldb import *
from annotation import spotlight, babelfy
from graph import graph, avgDegree, filteredResults

windows = "C:\\Users\kylek\PycharmProjects\Annotator/uploads"
mac = '/Users/jeff/PycharmProjects/Annotator/uploads'
UPLOAD_FOLDER = mac
ALLOWED_EXTENSIONS = set(['pdf','mp4','java','c'])

app = Flask(__name__)
db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '5d3bae549ae7c89b2d1be949'



def analysis(text):
    results=[]
    #print("Original text:", text)

    spotlightResults = spotlight(text)
    babelfyResults = babelfy(text)


    graphResults, initialConcepts = graph(spotlightResults, babelfyResults)
    # for g in graphResults:
    # print(g)
    # print()
    topTen = graphResults[:10]
    for t in topTen:
        t['frequency'] = ""
        # print(t)
        if t['camino'] == 'False':
            for i in initialConcepts:
                ending = i[0].rsplit('/', 1)[1]
                resource = "dbr:" + ending

                freq = i[1]
                # print(resource,t['label'])
                if resource == t['label']:
                    # print("as true")
                    t['frequency'] = freq
        else:
            oldSources = t['sources']
            t['sources'] = [s['label'] for s in topTen if s['label'] in oldSources]
            newSources = t['sources']
            t['frequency'] = 0
            for s in topTen:
                if s['label'] in newSources:
                    t['frequency'] += s['frequency']
            avgFreg = int(round(t['frequency'] / len(t['sources'])))
            t['frequency'] = avgFreg
        results.append(t)
        #print(t)



    '''
    #print("Original text:", text)

    spotlightResults, spotlightResultsAugmented = spotlight(text)

    #print("DBpedia Spotlight:", spotlightResults)
    #print("DBpedia Spotlight with words:", spotlightResultsAugmented)
    bablefyResults, babelfyResultsAugemented = babelfy(text)
    #print("Babelfy:", bablefyResults)
    #print("Babelfy with words:", babelfyResultsAugemented)

    graphResults = graph(spotlightResults,bablefyResults)
    #print("Graph:",graphResults )
    results = augmentedResults(graphResults, spotlightResultsAugmented, babelfyResultsAugemented)
    #print("AugmentedResults:", results)

    avg = avgDegree(results)
    #print("---filteredResults---")
    results =filteredResults(results, avg)'''
    return results


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process_txtfile', methods=['GET','POST'])
def process_txtfile():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        fileid = data['id']
        f = PDFDocument.query.filter_by(id=fileid).first()
        if f:
            concepts_exist = db.session.query(Concept).filter(pdf_concepts.c.pdf_id == f.id).all()

            if (len(concepts_exist) == 0):
                pages = Page.query.filter_by(id_pdf = f.id).all()
                print(pages)
                for page in pages:
                    path = page.path
                    print(path)
                    file = open(path, "r")
                    transcription = str(file.read())

                    if transcription != "":

                            concepts = analysis(transcription)
                            for con in concepts:
                                print(con)
                                resource = con['label']
                                print("resource: "+str(resource))
                                #words = con['word']
                                con_exist = Concept.query.filter_by(name=resource).first()
                                print("Before none:" + str(con_exist))
                                if con_exist == None:
                                    new_concept = Concept(name=resource)
                                    f.concepts.append(new_concept)

                                    print(new_concept,resource)
                                    con_exist = Concept.query.filter_by(name=new_concept.name).first()
                                    print("After none:" + str(con_exist))

                                cp = ConceptPages()
                                #cp.concept_id=con_exist.id
                                cp.degree=con['degree']
                                cp.pagerank=con['pagerank']
                                cp.camino = con['camino']
                                cp.frequency =con['frequency']
                                   # degree=, pagerank=con_exist['pagerank'],
                                  #                camino=con_exist['camino'], frequency=con_exist['frequency'])
                                cp.page = page
                                cp.concept=con_exist
                                con_exist.pages.append(cp)
                                #page.concepts.append(con_exist)
                                if con['camino'] == 'True':
                                    print("enter camino")
                                    sources = con['sources']
                                    print(sources)
                                    for s in sources:
                                        source = Concept.query.filter_by(name=s).first()
                                        print(source.id,con_exist.id,con_exist.name)

                                        link_exist = Link.query.filter_by(source_id=source.id,
                                                                          target_id=con_exist.id).first()
                                        print(link_exist)
                                        if link_exist==None:
                                            new_link = Link(source_id=source.id,target_id=con_exist.id)
                                            db.session.add(new_link)
                                            print(new_link.source_id,new_link.target_id )
                                            link_exist = Link.query.filter_by(source_id=new_link.source_id,
                                                                              target_id=new_link.target_id).first()
                                            print("After none:" + str(link_exist))

                                            #db.session.add(link_exist)
                                '''
                                for word in words:
                                    word_exist = Word.query.filter_by(name=word,id_concept=con_exist.id).first()
                                    if word_exist == None:
                                        new_word = Word(name=word)
                                        new_word.id_concept=con_exist.id
                                        db.session.add(new_word)
                                '''

        db.session.commit()

        annotations = db.session.query(Concept).filter(pdf_concepts.c.pdf_id == f.id).all()
        dict = [ object_as_dict(row) for row in annotations ]
        print(dict)

        for d in dict:
            c_id = d['id']
            d['pages']=[]
            print(d,c_id)
            #pages = db.session.query(ConceptPages).join(Page).filter()
            pages = db.session.query(Page).join(ConceptPages).filter(ConceptPages.concept_id == c_id and Page.id_pdf==f.id).all()
            for pa in pages:
                d["pages"].append("Page "+pa.number)


        print(dict)
        #res = make_response(jsonify(dict), 200)

        res = "ok"
        return res


@app.route('/process_file', methods=['GET','POST'])
def process_file():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        fileid = data['id']
        f = PDFDocument.query.filter_by(id=fileid).first()
        if f:
            print("id of file: "+str(f.id))

            myFileName, myFileExt = os.path.splitext(f.path)

            print(myFileName)
            print(myFileExt)



            if myFileExt.lower() == '.pdf':
                processPDF(f)
            res = make_response(jsonify({"message": "Processed "+str(f.name),"path":f.path,"filename":f.name,"id":f.id}), 200)

            return res


    return "11"

@app.route('/retrieve_data', methods=['GET','POST'])
def retrieve_data():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        fileid = data['id']
        annotations = db.session.query(Concept).filter(pdf_concepts.c.pdf_id == fileid).all()
        jsonres = json.dumps([ object_as_dict(row) for row in annotations ])

        res = make_response(jsonify(jsonres), 200)

        return res


@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    print("upload")

    if request.method == 'POST':
        print("post")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            destination = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(destination)
            #process_file(destination)
            f = PDFDocument.query.filter_by(name=filename).first()
            if f is None:
                f = PDFDocument(name=filename,path=destination)
                db.session.add(f)
                db.session.commit()
            print(f.id,f.name)


            res = make_response(jsonify({"message": "Uploaded "+str(f.name),"path":f.path,"filename":f.name,"id":f.id}),200)
            print(res)
            return res #redirect(url_for('uploaded_file',filename=filename))
    return  "11"
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
