import os

file_type_value = {'.txt':-3, '.docx':-2, '.tex':-1, '.pdf' : 0 , '.m' : 1 , '.py' : 2,\
                '.ipynb' :3 , '.mlx' : 4, '.log' :5, '.aux' : 6,}
tex_dir =  os.path.join('..', 'sample_tex_files')
tex_file_list = os.listdir(tex_dir)
print(tex_file_list)

file_types_dict = {}
# read main start tex file
tex_fname = os.path.join(tex_dir, 'main_start.tex')
fin = open(tex_fname , 'r')
tex_start_str = fin.read()
fin.close()
print(tex_start_str)

# read main pdf tex file
tex_fname_pdf = os.path.join(tex_dir, 'main_pdf.tex')
fin = open(tex_fname_pdf , 'r')
tex_pdf = fin.read()
fin.close()
print(tex_pdf)

# read main matlab tex file
tex_fname_matlab = os.path.join(tex_dir, 'main_matlab.tex')
fin = open(tex_fname_matlab , 'r')
tex_matlab = fin.read()
fin.close()
print(tex_matlab)



# read main python tex file
tex_fname_python = os.path.join(tex_dir, 'main_python.tex')
fin = open(tex_fname_python , 'r')
tex_python = fin.read()
fin.close()
print(tex_python)


# read main tex end file
# read main matlab tex file
tex_fname_end = os.path.join(tex_dir, 'main_end.tex')
fin = open(tex_fname_end , 'r')
tex_end = fin.read()
fin.close()
print(tex_end)

# read python tex file


base_dir = os.path.join('..', 'dsp_midsem', 'Working files')

dir_list = os.listdir(base_dir)
dir_list.sort()

print(dir_list)
cmd_del_list = []
for index, name in enumerate(dir_list[:], 0):
    inner_dir_path = os.path.join(base_dir, name)
    temp_file_list = os.listdir(inner_dir_path)
    if len(temp_file_list) >0:
        total_tex = ''
        section_name_pdf = ''
        section_name_matlab = ''
        section_name_python = ''
        section_name_end = ''
        inner_file_path = os.path.join(inner_dir_path, temp_file_list[0])
        inner_file_list = os.listdir(inner_file_path)

        inner_file_list.sort(key = lambda item : file_type_value['.' + item.split('.')[-1]] if '.' + item.split('.')[-1] in file_type_value else -100)
        print(index, name, inner_file_list)
        cmd = 'cp "{}" "{}"'.format(os.path.join(tex_dir,'mcode.sty') , '.')
        #print('CMD :', cmd)
        os.system(cmd)
        tex_start_str = tex_start_str.replace('TITLE', name)
        tex_start_str = tex_start_str.replace('NAME', name)
        #print(tex_start_str)

        for fname in inner_file_list[:]:
            file_type = fname.split('.')[-1]
            if file_type not in file_types_dict:
                file_types_dict[file_type] = {'count' : 0 , 'name_list' : []}
            file_types_dict[file_type]['count'] +=1
            if (index, name) not in file_types_dict[file_type]['name_list']:
                file_types_dict[file_type]['name_list'].append((index, name))
            if fname.endswith('.pdf'):
                section_str = fname.strip('.pdf').replace('_', ' ')
                section_name = tex_pdf.replace('SECTION NAME', section_str)
                section_name = section_name.replace('PDF NAME', os.path.join(inner_file_path, fname))
                section_name_pdf += section_name
                #print('section pdf : ',  section_name)
                # total_tex = tex_start_str + section_name_pdf
            elif fname.endswith('.m'):
                section_str = fname.strip('.m').replace('_', ' ')
                section_name = tex_matlab.replace('SECTION NAME', section_str)
                section_name = section_name.replace('MATLB FILENAME',  os.path.join(inner_file_path, fname))
                section_name_matlab += section_name
                #total_tex = tex_start_str + section_name_pdf
            elif fname.endswith('.py'):
                section_str = fname.strip('.py').replace('_', ' ')
                section_name = tex_python.replace('SECTION NAME', section_str)
                section_name = section_name.replace('PYTHON FILENAME',  os.path.join(inner_file_path, fname))
                section_name_python += section_name
                #print(inner_dir_path, fname)
            elif fname.endswith('.ipynb'):
                # convert .ipy nb to .py files
                cmd = 'jupyter nbconvert "{}" --to pdf'.format(os.path.join(inner_file_path, fname))
                os.system(cmd)
                # fname_new = fname.replace('.ipynb', '.py')
                # section_str = fname_new.strip('.py').replace('_', ' ')
                # section_name = tex_python.replace('SECTION NAME', section_str)
                # section_name = section_name.replace('PYTHON FILENAME',  os.path.join(inner_file_path, fname_new))
                # section_name_python += section_name

                # for including pdf files
                fname_new =  fname.replace('.ipynb', '.pdf')
                section_str = fname_new.strip('.pdf').replace('_', ' ')
                section_name = tex_pdf.replace('SECTION NAME', section_str)
                section_name = section_name.replace('PDF NAME', os.path.join(inner_file_path, fname_new))
                section_name_pdf += section_name
                #print(inner_dir_path, fname)
                cmd_del = 'rm "{}"'.format(os.path.join(inner_file_path, fname_new))
                cmd_del_list.append(cmd_del)
        total_tex_file = tex_start_str + section_name_pdf + section_name_matlab + section_name_python + tex_end
        #print(total_tex_file)


        fname_out = os.path.join(inner_file_path, name + '.tex')
        fout = open(fname_out, 'w')
        fout.write(total_tex_file)
        fout.close()
        print(' processed file : {}'.format(fname_out))
        cmd = 'pdflatex "{}"'.format(fname_out)
        print('\n \n \t \tCMD :', cmd)
        os.system(cmd)
        print(' \t\t converted to pdf files')
        for cmd_del in cmd_del_list:
            print('CMD del :', cmd_del)
            os.system(cmd_del)
        cmd_del_list = []

print('\t\ t Printing file type dict')
key_list = list(file_types_dict.keys())
print(key_list)
key_list.sort(key = lambda item :  file_type_value['.' + item.split('.')[-1]] if '.' + item.split('.')[-1] in file_type_value else -100)
print(key_list)
for file_type in key_list:
    print('.', file_type, '::\t', file_types_dict[file_type])
#print(' FILE type DICT', file_types_dict)
