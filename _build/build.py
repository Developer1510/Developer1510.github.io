import os
import sys
import traceback
import json
import glob
import re
import base64
import markdown
from PIL import Image

eob_base_url = 'https://apps.sentinel-hub.com/eo-browser/?'
max_theme_image_width = 240
max_theme_image_height = 200
max_pin_image_width = 640
max_pin_image_height = 480

texts_per_theme = {}
        
with open('_build/container.html', 'r', encoding='utf-8') as html_container_file, \
    open('_build/pin.html', 'r', encoding='utf-8') as html_pin_file:
    
    html_container_template = html_container_file.read()
    pin_html_template = html_pin_file.read()

    for pins_dir in os.listdir('.'):
        if os.path.isdir(pins_dir) and not pins_dir.startswith('_') and not pins_dir.startswith('.'):
            pin_auto_group_serial = 0
            pins_per_group = {}
            
            for pins_json_file_name in glob.glob(os.path.join(pins_dir, '*.json')):
                try:
                    with open(pins_json_file_name, 'r', encoding='utf-8') as pins_json_file:
                        print('Processing JSON file "' + pins_json_file_name + '"')
                        pins = json.load(pins_json_file)
                        for pin in pins:
                            pin_id = pin.get('_id') or ''
                            is_location = 'lat' in pin and 'lng' in pin
                            is_eob = is_location and 'zoom' in pin
                            
                            pin_lib_extra = pin.get('pinLibrary')
                            group = pin_lib_extra.get('group') if pin_lib_extra else None 
                            thumbnail_path = pin_lib_extra.get('thumbnailPath') if pin_lib_extra else None
                            if thumbnail_path is None and pin_id:
                                thumbnail_path = 'fig/' + pin_id + '.jpg'
                            download_url = pin_lib_extra.get('highResolutionImageUrl') if pin_lib_extra else None 
                            
                            # generate EOB URL
                            eob_url = eob_base_url
                            for pin_key in pin.keys():
                                if pin_key not in ('title', 'description', 'pinLibrary'):
                                    if pin_key == 'evalscript':
                                        eob_url += '&' + pin_key + '=' + base64.b64encode(bytes(str(pin.get(pin_key)), 'utf-8')).decode("utf-8")
                                    else:
                                        eob_url += '&' + pin_key + '=' + str(pin.get(pin_key))
                                        
                            
                            # if group not specified, use the JSON "_id" field, otherwise autogenerate the groupID
                            if not group:
                                if pin_id:
                                    group = '_$' + pin_id
                                else:
                                    group = '_$' + str(pin_auto_group_serial)
                                    pin_auto_group_serial += 1
                            
                            # get the group for this pin
                            pins_in_group = pins_per_group.get(group)
                            if not pins_in_group:
                                pins_in_group = []
                                pins_per_group[group] = pins_in_group
                            
                            # add current pin data to the group
                            pin_data = { \
                                'id': pin_id, \
                                'group': group, \
                                'is_location': is_location, \
                                'is_eob': is_eob, \
                                'title': pin.get('title') or '', \
                                'date': (pin.get('fromTime') or '')[:10], \
                                'type': pin.get('datasetId') or '', \
                                'thumbnail_path': thumbnail_path if thumbnail_path else '', \
                                'world_pos_x': str(int((pin['lng'] + 180) * 300 / 360)) if is_location else '0', \
                                'world_pos_y': str(int((-pin['lat'] + 90) * 150 / 180)) if is_location else '0', \
                                'eob_url': eob_url, \
                                'download_url': download_url if download_url else '', \
                                'description': markdown.markdown(pin['description']), \
                                'visible': 'true' \
                            }
                            pins_in_group.append(pin_data)    
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)               
            
            html_content = '\t\t\t\t\t<h2>Pins</h2>\n'
            javascript = '\t\t\tvar groups = [];\n'
    
            # put the first pin of each group into the HTML and append all pins to javascript
            for group in pins_per_group:
                pins_in_group = pins_per_group[group]
                
                html_pager = ''
                if len(pins_in_group) > 1:
                    for i in range(0, len(pins_in_group)):
                        pager_image = 'pager_current' if i == 0 else 'pager_other'
                        html_pager += '<img src="{layout_dir}/' + pager_image + '.png" id="' + group + '_pin' + str(i) + '" />'
                
                javascript += "\t\t\tgroups['" + group +"'] = {\n\t\t\t\t'pins':[\n"
                for pin in pins_in_group:
                    javascript += '\t\t\t\t\t{'
                    for pin_field in pin:
                        if not pin_field == 'group':
                            javascript += "'" + pin_field + "': '" + str(pin[pin_field]).replace("'", "\\'") + "', "
                    javascript += '},\n'
                javascript += '\t\t\t\t]\n\t\t\t};\n'
                
                pin = pins_in_group[0]
                
                html_content += pin_html_template \
                    .replace('{pager}', html_pager) \
                    .replace('{group}', pin['group']) \
                    .replace('{title}', pin['title']) \
                    .replace('{date}', pin['date']) \
                    .replace('{type}', pin['type']) \
                    .replace('{thumbnail_path}', pin['thumbnail_path'] if pin['thumbnail_path'] else '') \
                    .replace('{world_pos_x}', pin['world_pos_x']) \
                    .replace('{world_pos_y}', pin['world_pos_y']) \
                    .replace('{world_pos_display}', 'block' if pin['is_location'] else 'none') \
                    .replace('{eob_url}', pin['eob_url']) \
                    .replace('{eob_display}', 'block' if pin['is_eob'] else 'none') \
                    .replace('{download_url}', pin['download_url']) \
                    .replace('{download_display}', 'block' if pin['download_url'] else 'none') \
                    .replace('{description}', pin['description']) \
                    .replace('{arrow_right_display}', 'block' if len(pins_in_group) > 1 else 'none')
                    
                texts_in_theme = texts_per_theme.get(pins_dir)
                if texts_in_theme == None:
                    texts_in_theme = ""
                
                texts_in_theme += pin['title'] + " " + pin['description'] + " "
                texts_per_theme[pins_dir] = texts_in_theme
                
            html_content += '\t\t\t\t\t</div>\n'
            
            html = html_container_template.replace('{content}', html_content)
            html = html.replace('{script}', javascript)
            html = html.replace('{layout_dir}', '../_layout')
            html = html.replace('{github_repo_url}', sys.argv[1] if len(sys.argv) > 1 else 'https://www.github.com')

            output_html_file = open(os.path.join(pins_dir, 'index.html'), 'w', encoding='utf-8')
            output_html_file.write(html)
            output_html_file.close() 

print("Finished building HTML for pins")


with open('themes.json', 'r', encoding='utf-8') as themes_json_file, \
    open('_build/container.html', 'r', encoding='utf-8') as html_container_file, \
    open('_build/theme.html', 'r', encoding='utf-8') as html_theme_file:
    
    html = html_container_file.read()
    theme_html_template = html_theme_file.read()
    
    html_content = '\t\t\t\t\t<h2>Themes</h2>\n' + \
                    '\t\t\t\t\t<div id="themes">\n'
    
    themes = json.load(themes_json_file)
    for theme in themes:
        theme_name = theme['name']
        theme_path = re.sub('[^a-zA-Z0-9]', '_', theme_name)
        
        html_content += theme_html_template \
            .replace('{theme_path}', theme_path) \
            .replace('{theme_name}', theme_name)
        
        # resize and crop the images, that are too big 
        theme_image = Image.open('_themeimgs/' + theme_path + '.jpg')
        theme_image_width, theme_image_height = theme_image.size
        
        if (theme_image_width > max_theme_image_width) or (theme_image_height > max_theme_image_height):
            is_wide = theme_image_width > theme_image_height * max_theme_image_width / max_theme_image_height
            small_image_width = int(theme_image_width * max_theme_image_height / theme_image_height) if is_wide else max_theme_image_width
            small_image_height = int(theme_image_height * max_theme_image_width / theme_image_width) if not is_wide else max_theme_image_height
            small_image_horiz_border = (small_image_width - max_theme_image_width) / 2
            small_image_vert_border = (small_image_height - max_theme_image_height) / 2
            
            theme_image.thumbnail((small_image_width, small_image_height), Image.ANTIALIAS)
            small_image = theme_image.crop((small_image_horiz_border, small_image_vert_border, small_image_width - small_image_horiz_border, small_image_height - small_image_vert_border ))
            small_image.save('_themeimgs/' + theme_path + '.jpg', 'jpeg', quality=95)
            print('Resized theme image "' + theme_name + '" from ' + str(theme_image_width) + ' x ' + str(theme_image_height))
        
    
    html_content += '\t\t\t\t\t</div>\n'
    
    javascript = '\t\t\tvar texts = {};\n'
    for theme_name in texts_per_theme:
        javascript += '\t\t\ttexts["' + theme_name + '"] = "' + texts_per_theme[theme_name].replace('"', '\\"').replace('\n', ' ').replace('\r', ' ') + '";\n'

    html = html.replace('{content}', html_content)
    html = html.replace('{script}', javascript)
    html = html.replace('{layout_dir}', '_layout')
    html = html.replace('{github_repo_url}', sys.argv[1] if len(sys.argv) > 1 else 'https://www.github.com')

    output_html_file = open('index.html', 'w', encoding='utf-8')
    output_html_file.write(html)
    output_html_file.close()
    
print("Finished building HTML for themes")
