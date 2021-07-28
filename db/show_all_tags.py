import PySimpleGUI as sg
import os, datetime, tempfile, subprocess, platform, json, shutil, json
def rjson(a_path:str) -> dict: return json.loads('\n'.join([i for i in open(a_path, 'r', encoding='utf-8').readlines() if not i.strip().startswith('//')]))
wjson = lambda fpath, x: json.dump(x, open(fpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
rfile = readfile = lambda fpath: open(fpath, 'r', encoding='utf-8').read();
wfile = writefile = lambda fpath, x: open(fpath, 'w', encoding='utf-8').write(x)

from textwrap import dedent
info_extractor_code = lambda : dedent(r'''

    import psg as sg # SDK
    import os, datetime, inspect, json # python libs

    def rjson(a_path:str) -> dict: return json.loads('\n'.join([i for i in open(a_path, 'r', encoding='utf-8').readlines() if not i.strip().startswith('//')]))
    wjson = lambda fpath, x: json.dump(x, open(fpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); rfile = readfile = lambda fpath: open(fpath, 'r', encoding='utf-8').read(); wfile = writefile = lambda fpath, x: open(fpath, 'w', encoding='utf-8').write(x)

    if __name__ == '__main__':
        cd = CD = os.path.dirname(os.path.abspath(__file__))
        result_file = os.path.join(cd, 'psg_info_extractor.json')

        #
        # get input
        #
        def valid_field(pair):
            bad_fields = 'LOOK_AND_FEEL_TABLE copyright __builtins__'.split(' ')
            bad_prefix = 'TITLE_ TEXT_ ELEM_TYPE_ DEFAULT_ BUTTON_TYPE_ LISTBOX_SELECT METER_ POPUP_ THEME_'.split(' ')

            field_name, python_object = pair
            if type(python_object) is bytes:
                return False
            if field_name in bad_fields:
                return False
            if any([i for i in bad_prefix if field_name.startswith(i)]):
                return False

            return True
        #                                                                                       # ]
        psg_members  = [i for i in inspect.getmembers(sg) if valid_field(i)]        # ] 
        psg_funcs    = [o[0] for o in psg_members if inspect.isfunction(o[1])]                  # ] Grabing PSG objects
        psg_classes  = [o for o in psg_members if inspect.isclass(o[1])]                        # ] 
                # psg_props    = [o for o in psg_members if type(o[1]).__name__ == 'property']          # ]
        # I don't know how this magic filtering works, I just know it works. "Private" stuff (begins with _) are somehow
        # excluded from the list with the following 2 lines of code.  Very nicely done Kol-ee-ya!
        psg_classes = sorted(list(set([i[1] for i in psg_classes])), key=lambda x : x.__name__) # filtering of anything that starts with _ (methods, classes, etc)


        # 
        # 
        # 1 - processing classes
        # 
        # 

        class_messages=[]
        for aclass in psg_classes:
            class_name = aclass.__name__
            
            # filter bad objects
            if  'Tk' in class_name or 'TK' in class_name or\
                'Element' == class_name: # or 'Window' == class_name:
                continue
            
            # print standart things:
            class_messages.append(f'## {class_name} Element ')
            class_messages.append(f'<!-- <+{class_name}.doc+> -->')
            class_messages.append(f'<!-- <+{class_name}.__init__+> -->\n')

            # print all public methods:
            class_messages.append('\n'.join([f"### {name}\n<!-- <+{class_name}.{name}+> -->\n"
                                            for name, obj in inspect.getmembers(aclass)
                                            if not name.startswith('_')  ]))
        class_messages = '\n'.join(class_messages)

        # 
        # 
        # 2 - processing funcs
        # 
        # 
        def get_filtered_funcs(some_psg_funcs, show_underscore=False):
            space = '-'*30
            curr_dt = today = datetime.datetime.today()
            filtered = [f'{curr_dt}\n\n{space}Functions start here{space}\n']
            for i in some_psg_funcs:
                txt = f"<!-- <+func.{i}+> -->"

                if i.startswith('_') and show_underscore:
                    filtered.append(txt); continue
                filtered.append(txt)
            return f'TOTAL funcs amount listed below: {len(filtered)}\n' + '\n'.join(filtered)
        funcs_messages           = get_filtered_funcs(psg_funcs, True)
        funcs_messages__nodunder = get_filtered_funcs(psg_funcs, False)

        wjson(result_file, {
            'class_messages': class_messages,
            'funcs_messages'           : funcs_messages,
            'funcs_messages__nodunder' : funcs_messages__nodunder
        })
''')

tdir = tempfile.mkdtemp() # temp folder
import os
path = '/path/to/'
tdir = tempfile.mkdtemp() # temp folder
def get_info(psg_abspath):
    global tdir
    def sh(command,cwd=None):
        return subprocess.check_output(command, shell=True, cwd=cwd, executable='/bin/bash' if 'Linux' in platform.system() else None)

    # write SDK
    psg_py = os.path.join(tdir, f'psg.py')
    wfile(psg_py, rfile(psg_abspath))
    # write Extractor
    psg_info_extractor = os.path.join(tdir, f'psg_info_extractor.py')
    wfile(psg_info_extractor, info_extractor_code())



    # run Extractor
    python = 'python' if 'Windows' in platform.system() else 'python3'
    sh(f'{python} psg_info_extractor.py', cwd=tdir)

    return rjson(os.path.join(tdir, 'psg_info_extractor.json'))
    '''
        {
            'class_messages': [...]
            'funcs_messages'           : [...]
            'funcs_messages__nodunder' : [...]
        }
    '''
layout = [
    [sg.T('ABSOLUTE path to', font='Mono 14'), sg.T('PySimpleGUI.py:', key='psglbl', font='Mono 12')],
    [sg.I('', size=(30*5,1), enable_events=True, key='-psg_abspath-')],
    [sg.Combo([], size=(30*5,5), enable_events=True, key='-combo_psg_abspath-')],
    [sg.B('process', key='-process-')],

    [sg.ML(size=(80,40), key='mline1_classes'), sg.ML(size=(80,40), key='mline2_funcs')],
    [sg.CB('show _ funcs&methods?', key='-cbox-showFuncNMethods-', enable_events=True)],
]
window = sg.Window('All TAGS', layout, resizable=True, finalize=True)
last_info_created = None

def update_OSPATHEXISTS_color_of_psg(state=None):
    global window
    if not (state is None):
        window['psglbl'](text_color='#00ff0a' if state else 'red')
    else:
        window['psglbl'](text_color='#00ff0a' if window['-psg_abspath-'] else 'red')

def set_psg_path(fpath):
    global window
    window['-psg_abspath-'](fpath)
    update_OSPATHEXISTS_color_of_psg()







# 
# 
# local storage
# 
# 
localstorage = sg.UserSettings(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'))

# load last UI state
if list_of_files := localstorage.get('-last_psg_abspath_list-', []):
    window['-psg_abspath-'](list_of_files[-1])
    window['-combo_psg_abspath-'](values=list_of_files)
else:
    localstorage.set('-last_psg_abspath_list-',[])
update_OSPATHEXISTS_color_of_psg()






while True:
    event, values = window(timeout=100)
    if event in ('Exit', None):
        localstorage.save()
        break

    if event == '-combo_psg_abspath-': # CHANGED: current item in combo

        last_combo_val:str = values['-combo_psg_abspath-']
        if last_combo_val != values['-psg_abspath-']:
            window['-psg_abspath-'](last_combo_val)
            update_OSPATHEXISTS_color_of_psg()

    if event == '-psg_abspath-': # CHANGED: text
        psg_abspath = values['-psg_abspath-']
        psg_abspath_exists = os.path.exists(psg_abspath) and os.path.isfile(psg_abspath)
        
        # updates
        update_OSPATHEXISTS_color_of_psg(state=psg_abspath_exists)
        if psg_abspath_exists:
            if not localstorage:
                localstorage.set('-last_psg_abspath_list-', [psg_abspath])
                set_psg_path(psg_abspath)
            elif localstorage and localstorage.get('-last_psg_abspath_list-', 'NONE') != 'NONE':
                ll = localstorage.get('-last_psg_abspath_list-')
                if not ll:
                    localstorage['-last_psg_abspath_list-'] = [psg_abspath]
                    set_psg_path(psg_abspath)
                elif ll[-1] != psg_abspath:
                    localstorage['-last_psg_abspath_list-'].append(psg_abspath)
                    set_psg_path(psg_abspath)



    if event == '-process-': # btn pressed
        # take abspath
        # get metadata
        # output to elements
        psg_abspath = values['-psg_abspath-']
        if not os.path.exists(psg_abspath): continue

        psg_info = get_info(psg_abspath)
        if not psg_info: continue

        last_info_created = psg_info
        window['mline1_classes'](psg_info['class_messages'])
        window['mline2_funcs'](psg_info['funcs_messages'] if values['-cbox-showFuncNMethods-'] else psg_info['funcs_messages__nodunder'])

    if event == '-cbox-showFuncNMethods-':
        if not (last_info_created is None):
            txt = last_info_created['funcs_messages'] if values['-cbox-showFuncNMethods-'] else last_info_created['funcs_messages__nodunder']
            window['mline2_funcs'](txt)

window.close()

# rm all files, dir
[os.remove(i.path) for i in os.scandir(tdir) if i.is_file()]
shutil.rmtree(tdir)


