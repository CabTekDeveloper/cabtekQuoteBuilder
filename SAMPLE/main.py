from waitress import serve
from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from datetime import datetime
import os

import db_manager_cabtek_solutions as  cabtek_solutions_db
import db_manager_cabinet_parameters as cabinet_parameter_db
import helper
import file_folder_paths

app = Flask(__name__)
Bootstrap(app)

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/<int:issue_id>/<int:program_id>')
@app.route('/<int:program_id>')
@app.route('/')
def index(issue_id=None, program_id=None):
    all_programs = cabtek_solutions_db.get_all_programs()
    issues_by_prog_id = []
    files_by_issue_id = []
    program_name = ''
    if program_id != None:
        program_id = int(program_id)
        program_name = cabtek_solutions_db.get_prog_name_by_prog_id(program_id)
        issues_by_prog_id = cabtek_solutions_db.get_issues_by_prog_id(program_id) 

    if issue_id !=None:
        issue_id = int(issue_id)
        files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
    
    return render_template('index.html', home_selected=True, program_id=program_id, program_name=program_name,issue_id=issue_id, all_programs=all_programs, issues_by_prog_id=issues_by_prog_id, files_by_issue_id = files_by_issue_id,page_name = 'index')

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/add_issue', methods=['GET', 'POST'])
def add_issue():
    all_programs = cabtek_solutions_db.get_all_programs()

    if request.method == 'POST':
        helper.backup_db() # Wangchuk added 20-03-2025
        program_name = request.form.get('program_name')
        program_id = cabtek_solutions_db.get_prog_id_by_prog_name(program_name)
        issue_name = request.form.get('issue_name')
        cause = request.form.get('cause')
        solution = request.form.get('solution')
        example = request.form.get('example')
        added_by = request.form.get('added_by')
        current_issue_id = cabtek_solutions_db.insert_into_issues_table(program_id, issue_name, cause, solution, example,added_by)
        if current_issue_id != None:
            single_issue = cabtek_solutions_db.get_single_issue(current_issue_id)
            return render_template('add_uploads.html', single_issue = single_issue, program_name =program_name , page_name = 'add_issue')
    return render_template('add_issue.html', all_programs=all_programs, page_name = 'add_issue')

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/add_new_program_name/<return_url>', methods=['GET', 'POST'])
@app.route('/add_new_program_name/<return_url>/<int:issue_id>/<int:program_id>', methods=['GET', 'POST'])
def add_new_program_name(return_url=None, issue_id = None, program_id = None):
    all_programs = cabtek_solutions_db.get_all_programs()
    if request.method == "POST":
        new_program_name = request.form.get('new_program_name')
        cabtek_solutions_db.insert_into_programs_table(new_program_name)

        if return_url == 'add_issue':
            return redirect(url_for('add_issue'))
        
        elif return_url == 'edit_issue':
            return redirect(url_for('edit_issue',issue_id=issue_id,program_id=program_id))
        
    return render_template('add_new_program_name.html', all_programs=all_programs, return_url = return_url , issue_id = issue_id, program_id = program_id)

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/edit_issue/<int:issue_id>/<int:program_id>', methods=['GET','POST'])
def edit_issue(issue_id=None, program_id=None):
    single_issue = cabtek_solutions_db.get_single_issue(issue_id)
    program_name = cabtek_solutions_db.get_prog_name_by_prog_id(program_id)
    all_programs = cabtek_solutions_db.get_all_programs()
    files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
    if request.method == "POST":
        program_name = request.form.get('program_name')
        program_id = cabtek_solutions_db.get_prog_id_by_prog_name(program_name)
        issue_name = request.form.get('issue_name')
        cause = request.form.get('cause')
        solution = request.form.get('solution')
        example = request.form.get('example')
        added_by = request.form.get('added_by')
        cabtek_solutions_db.update_issue(issue_id,program_id, issue_name, cause, solution, example,added_by)

        return redirect(url_for('index',issue_id=issue_id,program_id=program_id))
    
    return render_template('edit_issue.html', program_name=program_name,single_issue=single_issue,all_programs=all_programs, files_by_issue_id =files_by_issue_id)

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/delete_issue/<int:issue_id>/<int:program_id>')
def delete_issue(issue_id=None, program_id=None):
    # get all files for this issue and delete them from the folder
    files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
    if len(files_by_issue_id) > 0:
        for file in files_by_issue_id:
            file_path = f"static/{file['file_path']}"
            # delete file from the folder
            if os.path.exists(file_path):
                os.remove(file_path)

    #  delete all entries from files_table for the current issue_id
    cabtek_solutions_db.delete_files_using_issue_id(issue_id)

    # delete issue from the issue_tables
    cabtek_solutions_db.delete_single_issue(issue_id)

    return redirect(url_for('index', program_id = program_id))

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/edit_program_name', methods=['GET','POST'])
def edit_program_name():
    all_programs = cabtek_solutions_db.get_all_programs()

    if request.method == "POST":
        program_name = request.form.get('program_name')
        new_program_name = request.form.get('new_program_name').strip()
        program_id = cabtek_solutions_db.get_prog_id_by_prog_name(program_name)
        cabtek_solutions_db.update_program_name(program_id,new_program_name)
        all_programs = cabtek_solutions_db.get_all_programs()
    return render_template('edit_program_name.html', all_programs=all_programs , page_name = 'edit_program_name')

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/get_all_issues_using_prog_id', methods=['GET','POST'])
def get_all_issues_using_prog_id():
    issues_by_prog_id = []
    if request.method == "POST":
        program_name = request.form.get('program_name').strip()
        program_id = cabtek_solutions_db.get_prog_id_by_prog_name(program_name)
        issues_by_prog_id = cabtek_solutions_db.get_issues_by_prog_id(program_id)
        all_programs = cabtek_solutions_db.get_all_programs()
    return render_template('edit_program_name.html', all_programs=all_programs,issues_by_prog_id=issues_by_prog_id, show_yesNo_div = True, program_name = program_name, page_name = 'edit_program_name')

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/delete_issues_using_prog_id/<program_name>')
def delete_issues_using_prog_id(program_name):
    program_id = cabtek_solutions_db.get_prog_id_by_prog_name(program_name)
    issues_by_prog_id = cabtek_solutions_db.get_issues_by_prog_id(program_id)
    
    # this block will delete entries from files_table and files saved in uploads folder for the current program_name/program_id
    if len(issues_by_prog_id) > 0:
        for issue in issues_by_prog_id:
            issue_id = issue['issue_id']
          
            files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
            if len(files_by_issue_id) > 0:
                for file in files_by_issue_id:
                    file_path = f"static/{file['file_path']}"
                    # delete files from the folder
                    if os.path.exists(file_path):
                        os.remove(file_path)
            #  delete all entries from files_table for the current issue_id
            cabtek_solutions_db.delete_files_using_issue_id(issue_id)

    # delete issues from issues_table and entry in programs_table for the current program_name/program_id
    cabtek_solutions_db.delete_issues_by_prog_id(program_id)
    cabtek_solutions_db.delete_program_by_prog_id(program_id)
    return redirect(url_for('edit_program_name'))
    

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/upload_file/<int:issue_id>')
@app.route('/upload_file/<int:issue_id>/<file_type>', methods=['POST', 'GET'])
def upload_file(issue_id,file_type=None):
    files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
    single_issue = cabtek_solutions_db.get_single_issue(issue_id)
    program_name = cabtek_solutions_db.get_prog_name_by_prog_id(single_issue['program_id'])
    message = ""
    if request.method == "POST":
        image_file_extensions =  ["JPG","JPEG","PNG"]
        video_file_extensions =  ["MP4","WEBM","OGG"]
        file_obj = request.files.get("file_obj")
        file_obj_extension = file_obj.filename.split(".")[1]

        if file_type == "image":
            if (file_obj_extension.upper() in image_file_extensions):
                file_name = secure_filename(file_obj.filename)
                file_save_location = f"static/uploads/image/{file_name}"
                # If you look at the path below, you will notice that static has been removed. 
                # This is done so that we can add this to img src in show_file.html
                file_path = f"uploads/image/{file_name}" 

                if not os.path.exists(file_save_location):
                    file_obj.save(file_save_location)
                    cabtek_solutions_db.insert_into_files_table(issue_id,file_type,file_path)
                    files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
                    message = f"The file '{file_obj.filename}' has been uploaded successfully. Click Add Images or Add Videos to upload more files."
                else:
                    message = f"Could not upload the file '{file_obj.filename}' because a file with same name exists already. Rename the file and upload again."
            else:
                message = f"Could not upload the file '{file_obj.filename}'.The supported image formats are {','.join(image_file_extensions)}"

        elif file_type == "video":
            if (file_obj_extension.upper() in video_file_extensions):
                file_name = secure_filename(file_obj.filename)
                file_save_location = f"static/uploads/video/{file_name}"
                file_path = f"uploads/video/{file_name}"

                if not os.path.exists(file_save_location):
                    file_obj.save(file_save_location)
                    cabtek_solutions_db.insert_into_files_table(issue_id,file_type,file_path)
                    files_by_issue_id = cabtek_solutions_db.get_files_by_issue_id(issue_id)
                    message = f"The file '{file_obj.filename}' has been uploaded successfully. Click Add Images or Add Videos to upload more files."
                else:
                    message = f"Could not upload the file '{file_obj.filename}' because a file with same name exists already. Rename the file and upload again."
            else:
                message = f"Could not upload the file '{file_obj.filename}'.The supported video formats are {','.join(video_file_extensions)}"
        else:
            pass


        return render_template("add_uploads.html",single_issue = single_issue, program_name =program_name,message = message, page_name = 'add_issue', files_by_issue_id = files_by_issue_id)

    return render_template("add_uploads.html",single_issue = single_issue, program_name =program_name, files_by_issue_id = files_by_issue_id)

# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/show_file/<int:file_id>' , methods=['POST', 'GET'])
def show_file(file_id):
    single_file = cabtek_solutions_db.get_single_file(file_id)
    return render_template('show_file.html', single_file = single_file )
    
# CabTek Solutions Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/delete_file/<int:issue_id>/<int:program_id>/<int:file_id>')
def delete_file(issue_id,program_id,file_id):
    single_file = cabtek_solutions_db.get_single_file(file_id)
    file_path = f"static/{single_file['file_path']}"
    # delete file from the folder
    if os.path.exists(file_path):
        os.remove(file_path)
        # delete etry from the files_table
    cabtek_solutions_db.delete_single_file(file_id)

    return redirect(url_for('edit_issue',issue_id=issue_id,program_id=program_id))


#Cabinet Params : Routes-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/cp_home')
def cp_home():
    if request.method == "GET":
        all_product_types = cabinet_parameter_db.get_all_product_types()
        return render_template("cp_home.html", all_product_types=all_product_types)

#Cabinet Params : API-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/get_all_products_db' , methods=["GET"])
def get_all_products_db():
    try:
        if request.method == "GET":
            return jsonify(cabinet_parameter_db.get_all_products())
    except Exception as ex:
        return jsonify(ex)


@app.route('/get_all_part_names_db' , methods=["GET"])
def get_all_part_names_db():
    try:
        if request.method == "GET":
            return jsonify(cabinet_parameter_db.get_all_parts())
    except Exception as ex:
        return jsonify(ex)
    
    
@app.route('/get_all_cnccodes_db' , methods=["GET"])
def get_all_cnccodes_db():
    try:
        if request.method == "GET":
            return jsonify(cabinet_parameter_db.get_all_cnccodes())
    except Exception as ex:
        return jsonify(ex)
      

@app.route('/get_all_parameters_db' , methods=["GET"])
def get_all_parameters_db():
    try:
        if request.method == "GET":
            return jsonify(cabinet_parameter_db.get_all_parameters())
    except Exception as ex:
        return jsonify(ex)

@app.route('/get_all_images_db' , methods=["GET"])
def get_all_images_db():
    try:
        return jsonify(cabinet_parameter_db.get_all_images())
    except Exception as ex:
        return jsonify(ex)

@app.route('/get_product_info_db/<product_id>', methods=["GET"])
def get_product_info_db(product_id):
    try:
        if request.method == "GET":
            product_info = cabinet_parameter_db.build_product_info(product_id)
            return jsonify(product_info)
        
    except Exception as ex:
        return jsonify(ex)


@app.route('/get_cnccode_info_db/<cnccode_id>', methods=["GET"])
def get_cnccode_info_db(cnccode_id):
    try:
        if request.method == "GET":
            cnccode_info = cabinet_parameter_db.build_cnccode_info(cnccode_id)
            return jsonify(cnccode_info)
        
    except Exception as ex:
        return jsonify(ex)


@app.route('/get_parameter_info_db/<parameter_id>', methods=["GET"])
def get_parameter_info_db(parameter_id):
    try:
        if request.method == "GET":
            parameter_info = cabinet_parameter_db.build_parameter_info(parameter_id)
            return jsonify(parameter_info)
        
    except Exception as ex:
        return jsonify(ex)


@app.route('/update_product_parts_db', methods=['GET', 'POST'])
def update_product_parts_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            cabinet_parameter_db.update_product_parts_in_tbl_product_info(data)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)

@app.route('/update_part_cnccodes_db', methods=['GET', 'POST'])
def update_part_cnccodes_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            product_id  = data['product_id']
            part_id     = data['part_id']
            cnccodes    = data['cnccodes']
            cnccode_ids = [cnccode['id'] for cnccode in cnccodes]
            cabinet_parameter_db.update_cnccode_ids_in_tbl_product_info(product_id, part_id, cnccode_ids)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
    
@app.route('/update_cnccode_parameters_db', methods=['GET', 'POST'])
def update_cnccode_parameters_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            cnccode_id    = data['cnccode_id']
            parameters    = data['parameters']
            parameter_ids = [parameter['id'] for parameter in parameters]
            cabinet_parameter_db.update_parameter_ids_in_tbl_cnccode(cnccode_id, parameter_ids)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
 
 
#  
@app.route('/update_cnccode_description_db', methods=['POST'])
def update_cnccode_description_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            cnccode_id    = data['cnccode_id']
            description    = data['description']
            cabinet_parameter_db.update_description_in_tbl_cnccode(cnccode_id, description)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
       
@app.route('/update_cnccode_images_db', methods=['GET', 'POST'])
def update_cnccode_images_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            cnccode_id    = data['cnccode_id']
            images    = data['images']
            image_ids = [image['id'] for image in images]
            cabinet_parameter_db.update_image_ids_in_tbl_cnccode(cnccode_id, image_ids)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)


@app.route('/insert_new_part_db', methods=['POST'])
def insert_new_part_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            new_name    = data['name']
            cabinet_parameter_db.insert_into_tbl_part(new_name)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
    
    
@app.route('/insert_new_cnccode_db', methods=['POST'])
def insert_new_cnccode_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            new_name    = data['name']
            cabinet_parameter_db.insert_into_tbl_cncCode(new_name)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)

    
@app.route('/insert_new_parameter_db', methods=['POST'])
def insert_new_parameter_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            new_name    = data['name']
            cabinet_parameter_db.insert_into_tbl_parameter(new_name)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
    # insert_new_part_db
@app.route('/update_parameter_description_db', methods=['POST'])
def update_parameter_description_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            parameter_id    = data['parameter_id']
            description    = data['description']
            cabinet_parameter_db.update_description_in_tbl_parameter(parameter_id, description)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
    
@app.route('/update_parameter_images_db', methods=['GET', 'POST'])
def update_parameter_images_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            parameter_id    = data['parameter_id']
            images    = data['images']
            image_ids = [image['id'] for image in images]
            cabinet_parameter_db.update_image_ids_in_tbl_parameter(parameter_id, image_ids)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)

@app.route('/update_parameter_values_db', methods=['POST'])
def update_parameter_values_db():
    try:
        if request.method == "POST":
            data = request.get_json()
            parameter_id    = data['parameter_id']
            default_value = data['default_value']
            min_value = data['min_value']
            max_value = data['max_value']
            
            cabinet_parameter_db.update_parameter_values_in_tbl_parameter(parameter_id, default_value, min_value, max_value)
            return jsonify(success=True)
    
    except Exception as ex:
        return jsonify(ex)
    
@app.route('/save_image_db', methods=['POST'])
def save_image_db():
    try:
        if request.method == "POST":
            img_obj = request.files['data']
            if ( cabinet_parameter_db.save_image_in_folder_and_tbl_images(img_obj)):
                return jsonify({"saved": True, "message": "File uploaded!" })
            else:
                return jsonify({"saved": False, "message": "File not uploaded!\nPlease rename the file and upload again." })
        
    except Exception as ex:
        return jsonify({"saved": False, "message": "File not uploaded!"})

# 
#Run Server-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
if __name__ == "__main__":
    # serve(app,host='0.0.0.0', port=8002)              # For deploying
    app.run(host='0.0.0.0', port=8002, debug=True)      # For Testing

# Important: Before deploying do the following.
            # Change server to serve
            # Copy over the uploads folder from the previous live version into this version

###-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###