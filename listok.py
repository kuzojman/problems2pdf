import os.path
import tempfile
import shutil
import sys
import subprocess

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

def compile(latex_text, aux_files):
    with tempfile.TemporaryDirectory() as td:
        latex_fname = os.path.join(td, 'main.tex')
        with open(latex_fname, 'w') as f:
            f.write(latex_text)
        for fname in aux_files:
            shutil.copyfile(fname, os.path.join(td, os.path.basename(fname)))
        if sys.platform.startswith('linux'):
            cmd = 'pdflatex'
        else:
            cmd = 'pdflatex'

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
        listok = get_listok(self.template, problems)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        res = compile(listok, [os.path.join(cur_dir, 'logo.png')])
        print(os.path.join(cur_dir, 'logo.png'))
        return res


if __name__ == '__main__':
    import json
    template = get_template()
    with open('sample.json') as f:
        problems = json.load(f)
    listok = get_listok(template, problems)
    compile(listok, ['logo.png'])
    

            
