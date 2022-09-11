import os.path
import tempfile
import shutil
import sys
import subprocess
import requests
import re





def get_template(template_name=None):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    template_name = template_name or os.path.join(cur_dir, 'template.tex')
    with open(template_name) as f:
        return f.read()

def get_listok(template, problems, td):
    def make_problem(problem):
        s = ''
        s += '\\begin{Large} \n'
        s += '~\\\ \n'
        s += ('Задание №' + str(problem['id']) + '\n')
        s += '\end{Large}\n'
        s += '~\\\ \n'
        s += problem['task']
        if "image" in problem:
            url = problem['image']
            response = requests.get(url, stream=True)
            type_of_file = response.headers['Content-Type']


            if type_of_file=='image/png':
                fname = str(problem['id'])+'image.png'


            fullname = os.path.join(td, fname)


            with open(fullname, "wb") as handle:
                for data in response.iter_content():
                    handle.write(data)
            s += '~\\\ \n'
            s+= '\includegraphics[width=.4\linewidth]'             
            s += '{'+fname+'}'   
        #except:
        #    pass
        return s



    problems = [make_problem(problem) for problem in problems]
    delim = '~\\\ \n' + '~\\\ \n'
    problems = delim.join(problems)
    return template.replace('<PROBLEMS>', problems)

def compile(latex_text, aux_files, td):
    
        latex_fname = os.path.join(td, 'main.tex')
        with open(latex_fname, 'w') as f:
            f.write(latex_text)
        for fname in aux_files:
            shutil.copyfile(fname, os.path.join(td, os.path.basename(fname)))
        if sys.platform.startswith('linux'):
            cmd = 'pdflatex'
        else:
            cmd = 'pdflatex'
        for _ in range(2):
            subprocess.run([cmd, latex_fname], cwd=td)

        # subprocess.run(['pwd',], cwd=td)


        #with open(os.path.join(td, 'main.log'), 'r') as fb:
        #    print(fb.read())

        with open(os.path.join(td, 'main.pdf'), 'rb') as fb:
            return fb.read()
        # shutil.copyfile(os.path.join(td, 'main.pdf'), 'main.pdf')
        # print(td)

class LaTeXProcessor:
    def __init__(self, template_name=None):
        self.template = get_template(template_name)

    def __call__(self, problems):
        with tempfile.TemporaryDirectory() as td:
            listok = get_listok(self.template, problems, td)

            cur_dir = os.path.dirname(os.path.abspath(__file__))
            res = compile(listok, [os.path.join(cur_dir, 'logo.png')], td)
        print(os.path.join(cur_dir, 'logo.png'))
        return res


if __name__ == '__main__':
    import json

    lp = LaTeXProcessor()
    with open('sample.json') as f:
        problems = json.load(f)
    pdf_data = lp(problems)
    with open('sample_pdf.pdf', "wb") as f:
        f.write(pdf_data)

    

            
