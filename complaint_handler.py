import re
import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request

from complaint_service import ComplaintService
from complaint_class import Complaint

complaint = Blueprint('complaint',__name__)
complaint.service = ComplaintService()

def getHTMLText(pure_html):
    cleanr = re.compile('<.*?>')
    pure_text = re.sub(cleanr, '', pure_html)
    return pure_text

@complaint.route('/complaint/init')
def init_complaint_tbl():
    if request.method == 'GET':
        try:
            complaint.service.init_complaint_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@complaint.route('/complaint', methods = ['GET', 'POST'])
def get_complaints():
    if request.method == 'GET':
        all_complaints = complaint.service.get_all_complaints()
        return render_template('complaint.html',all_complaints = all_complaints)
    else:
        if request.json['op'] == 'delete':
            try:
                complaint.service.delete_complaint(request.json['complaint_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                complaint_search_result = complaint.service.get_complaints_by_name(request.json['complaint_text'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : complaint_search_result})
        elif request.json['op'] == 'update':
            try:
                complaint.service.update_complaint(request.json['complaint_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000'})
@complaint.route('/complaint/add', methods = ['GET', 'POST'])
def add_complaint():
    if request.method == "POST":
        errList = [];
        if getHTMLText(request.json['complaint_text']) == "":
            errList.append("Complaint Content cannot be empty!")
        if len(errList) != 0:
            return jsonify({
                'status' : 'FAIL',
                'errcode': errList
                })
        complaintObject = Complaint(request.json['complaint_text'], request.json['complaint_object'], request.json['complaint_object_id'], request.json['user_id'])
        try:
            complaint.service.add_complaint(complaintObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@complaint.route('/complaints/<int:complaint_id>', methods = ['GET', 'POST'])
def get_complaint(complaint_id):
    if request.method == 'GET':
        complaintObject = complaint.service.get_complaint(complaint_id)
        return render_template('edit_complaint.html',complaintObject = complaintObject)
    else:
        if getHTMLText(request.json['complaint_text']) == "":
            return jsonify({'status' : 'FAIL', 'errcode' : '00001'})
        try:
            complaint.service.update_complaint(complaint_id, request.json['complaint_text'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
        return jsonify({'status' : 'OK', 'errcode' : '00000'})




