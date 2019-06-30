from make_real_readme import main

########################################################################
#                              __ _            _                       #
#                             / _(_)          | |                      #
#    __   __   ___ ___  _ __ | |_ _  __ _     | |__   ___ _ __ ___     #
#    \ \ / /  / __/ _ \| '_ \|  _| |/ _` |    | '_ \ / _ \ '__/ _ \    #
#     \ V /  | (_| (_) | | | | | | | (_| |    | | | |  __/ | |  __/    #
#      \_/    \___\___/|_| |_|_| |_|\__, |    |_| |_|\___|_|  \___|    #
#                                    __/ |                             #
#                                   |___/                              #
########################################################################
enable_popup = not True
# method = 'simple, no log'
method = 'with logs'

##############
#     __     #
#    /_ |    #
#     | |    #
#     | |    #
#     | |    #
#     |_|    #
##############
if method == 'simple, no log':
    main(logger=None,
         files_to_include=[0, 1, 2, 3],
         output_name='This_is_FINAL_readme.md',
         delete_html_comments=True)

################
#     ___      #
#    |__ \     #
#       ) |    #
#      / /     #
#     / /_     #
#    |____|    #
################
if method == 'with logs':
    import logging; logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)
    my_file = logging.FileHandler('usage.log.txt', mode='w'); my_file.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s>%(levelname)s: %(message)s')
    my_file.setFormatter(formatter); logger.addHandler(my_file); logger.info('STARTING')
    main(logger=logger, files_to_include=[0, 1, 2, 3],
         output_name='This_is_FINAL_readme.md',
         delete_html_comments=True)

########################################
#     _____                            #
#    |  __ \                           #
#    | |__) |__  _ __  _   _ _ __      #
#    |  ___/ _ \| '_ \| | | | '_ \     #
#    | |  | (_) | |_) | |_| | |_) |    #
#    |_|   \___/| .__/ \__,_| .__/     #
#               | |         | |        #
#               |_|         |_|        #
########################################
if enable_popup:
    import PySimpleGUI as sg
    sg.Popup('DOCS ARE BAKED')
