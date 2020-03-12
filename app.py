from time import sleep
# from flask import Flask, request, jsonify, json
from flask import render_template, Flask, jsonify, json, request
import main
from src import get_output_data, create_er_xml_file
from src.utils import file_manipulation, git_push_automation

app = Flask(__name__)
text = ''


class MyObj(object):
    def __init__(self, entityname, attributelist):
        self.entityname = entityname
        self.attributelist = attributelist


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        if request.form['submit_btn'] == 'generate_entity_attribute':
            text = request.form['scenario']
            with open(file_manipulation.PATH + '\\input_text.txt', 'w+') as text_file:
                text_file.write(text)
            entitylist = main.generateEntities(text)
            return render_template('home.html', scenario=text, entitylist=entitylist)

        if request.form['submit_btn'] == 'generate_attribute':
            text = request.form['scenario']
            entitylist = request.form['entitylist']
            output = main.generateAttributes(text, entitylist)
            entitylist1 = []
            for entity in output:
                entitylist1.append(entity)
            my_objects = []
            for entity in output:
                my_objects.append(MyObj(entity, output[entity]))
            return render_template('home.html', scenario=text, entitylist=entitylist, my_objects=my_objects)

        if request.form['submit_btn'] == 'generate_final_list':
            text = request.form['scenario']
            finallist = request.form['attributelist']
            output = main.generateOutput(finallist)
            entitylist1 = list(output.keys())
            outputentitylist1 = []
            for entity in output:
                outputentitylist1.append(entity)
            my_objects = []
            for entity in output:
                my_objects.append(MyObj(entity, output[entity]))
            return render_template('home.html', scenario=text, entitylist=entitylist1, entitylist1=finallist,
                                   my_objects=my_objects)


@app.route('/api/v1/relationships', methods=['GET'])
def return_er_data():
    main.create_er_diagram_xml_file()
    sleep(10)
    relationship_data = get_output_data.get_relationship_list()
    print("Successfully Generated ER Diagram")
    print(relationship_data)
    return jsonify(relationship_data)


@app.route('/api/v1/schema', methods=['GET'])
def generate_relational_schema():
    sleep(10)
    main.create_relational_schema()
    return jsonify({"success": "true", "error": "false"})


@app.route('/api/v1/csv', methods=['POST'])
def create_er_csv():
    data = json.loads(request.data)
    sleep(10)
    create_er_xml_file.recreate_relation_xml(data)
    if data is None:
        return jsonify({"success": "false", "error": "true", "message": "JSON not found"})
    else:
        main.create_er_diagram_text_file()
        sleep(10)
        output = git_push_automation.git_push_automation()
        if output:
            return jsonify({"success": "true", "error": "false"})
        else:
            return jsonify({"success": "false", "error": "true", "message": "JSON not found"})


@app.route('/api/v1/clear', methods=['GET'])
def clear_files():
    file_manipulation.remove_files()
    return jsonify({"success": "true", "error": "false"})


if __name__ == '__main__':
    app.run(debug=True)
