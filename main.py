import sys
import os
import datetime
import random
import codecs
from app import app,now
from flask import Flask, render_template, request,session, jsonify,redirect,url_for,jsonify,send_from_directory
from models import *
from forms import RegistrationForm,adding_form,adding_text_to_post_form,adding_new_task_form,send_samples_to_student_form,Change_role,Comment_add,query_from_string,save_phone_form


import matplotlib.pyplot as plt


def get_template(template_name=None):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    template_name = template_name or os.path.join(cur_dir, 'template.tex')
    with open(template_name) as f:
        return f.read()

def get_listok(template, problems):

    def make_problem(problem):
        s = ''
        s += '\\begin{Large} \n'
        s += '~\\\ \n'
        s += ('Задание №' + str(problem['id']) + '\n')
        s += '\end{Large}\n'
        s += '~\\\ \n'
        s += problem['task']
        return s

    problems = [make_problem(problem) for problem in problems]
    delim = '~\\\ \n' + '~\\\ \n'
    problems = delim.join(problems)
    return template.replace('<PROBLEMS>', problems)

    

            




head_of_tex_file = '\\documentclass{article}%\n'+\
                   '\\usepackage[T1]{fontenc}%\n'+\
                   '\\usepackage[utf8]{inputenc}%\n'+\
                   '\\DeclareUnicodeCharacter{2220}{\ensuremath\\angle}%\n'+\
                   '\\usepackage{lmodern}%\n'+\
                   '\\usepackage{textcomp}%\n'+\
                   '\\usepackage{lastpage}%\n'+\
                   '\\usepackage{background}%\n'+\
                   '\\backgroundsetup{contents=\includegraphics{logo},opacity=0.45,scale=3}%\n'+\
                   '\\usepackage[russian]{babel}%\n'+\
                   '\\usepackage{geometry} %\n'+\
                   '\\geometry{a4paper, total={170mm,257mm},left=20mm,top=20mm,}%\n'+\
                    '\\DeclareUnicodeCharacter{2212}{-}%\n'+\
                   '%\n'+\
                   '\\begin{document}\n'




@app.route("/pdf_render/")
def render_pdf():
    list_of_ids = session["list_of_ids"]
    print(">>!!", list_of_ids)
    file_name = "tas"
    with codecs.open(file_name+'.tex', 'w', 'utf-8') as file:
        file.write(head_of_tex_file)
        for i in list_of_ids:
            tas = (Tasks.query.filter(Tasks.id == int(i)).first())

            file.write('\\begin{Large} \n')
            file.write('~\\\ \n')
            file.write('Задание №' + str(tas.id) + '\n')
            file.write('\end{Large}\n')
            file.write('~\\\ \n')
            task_print = tas.task
            task_print = task_print.replace('%','\%')
            file.write(task_print + '\n')
            file.write('~\\\ \n')
            file.write('~\\\ \n')
        file.write('\\end{document}\n')

    if sys.platform.startswith('linux'):
        cmd = '/usr/bin/pdflatex'
    else:
        cmd = 'pdflatex'
    os.system(f"{cmd}  {file_name}.tex")
    filepath = os.path.abspath(os.getcwd())
    return send_from_directory(filepath, file_name+'.pdf')
