import os
import json
import glob
import re
import base64
import markdown
from PIL import Image

eob_base_url = 'https://apps.sentinel-hub.com/eo-browser/?'
max_pin_image_width = 640
max_pin_image_height = 480


with open('_build/container.html', 'r', encoding='utf-8') as html_container_file, \
    open('_build/pin.html', 'r', encoding='utf-8') as html_pin_file:
    
    html_container_template = html_container_file.read()
    pin_html_template = html_pin_file.read()
    pin_serial = 0
    javascript = ''
    
    for pins_dir in os.listdir('.'):
        if os.path.isdir(pins_dir) and not pins_dir.startswith('_') and not pins_dir.startswith('.'):
            html_content = '\t\t\t\t\t<h2>Pins</h2>\n' + \
                            '\t\t\t\t\t<div id="pins">\n'
    
            for pins_json_file_name in glob.glob(os.path.join(pins_dir, '*.json')):
                with open(pins_json_file_name, 'r', encoding='utf-8') as pins_json_file:
                    pins = json.load(pins_json_file)
                    for pin in pins:
                        is_location = 'lat' in pin and 'lng' in pin
                        is_eob = is_location and 'zoom' in pin
                        pin_lib_extra = pin.get('pinLibrary')
                        thumbnail_path = pin_lib_extra.get('thumbnailPath') if pin_lib_extra else None 
                        
                        eob_url = eob_base_url
                        for pin_key in pin.keys():
                            if pin_key not in ('title', 'description', 'pinLibrary'):
                                if pin_key == 'evalscript':
                                    eob_url += '&' + pin_key + '=' + base64.b64encode(bytes(str(pin.get(pin_key)), 'utf-8')).decode("utf-8")
                                else:
                                    eob_url += '&' + pin_key + '=' + str(pin.get(pin_key))
                          
                        # print(eob_url)
                        
                        download_url = pin.get('visualizationUrl') or ''
                
                        html_content += pin_html_template \
                            .replace('{id}', 'pin' + str(pin_serial)) \
                            .replace('{title}', pin.get('title') or '') \
                            .replace('{date}', pin.get('toTime') or '') \
                            .replace('{type}', pin.get('datasetId') or '') \
                            .replace('{image_path}', thumbnail_path if thumbnail_path else '') \
                            .replace('{world_pos_x}', str(int((pin['lng'] + 180) * 300 / 360)) if is_location else '0') \
                            .replace('{world_pos_y}', str(int((-pin['lat'] + 90) * 150 / 180)) if is_location else '0') \
                            .replace('{world_pos_display}', 'block' if is_location else 'none') \
                            .replace('{eob_url}', eob_url) \
                            .replace('{eob_display}', 'block' if is_eob else 'none') \
                            .replace('{download_url}', download_url) \
                            .replace('{download_display}', 'block' if download_url else 'none') \
                            .replace('{description}', markdown.markdown(pin['description']))
                            
                        pin_serial += 1
                
            html_content += '\t\t\t\t\t</div>\n'
        
            html = html_container_template.replace('{content}', html_content)
            html = html.replace('{script}', javascript)
            html = html.replace('{layout_dir}', '../_layout')

            output_html_file = open(os.path.join(pins_dir, 'index.html'), 'w', encoding='utf-8')
            output_html_file.write(html)
            output_html_file.close() 

print("Finished building HTML for pins")
