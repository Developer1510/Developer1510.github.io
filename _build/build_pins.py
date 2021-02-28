import os
import json
import glob
import re
import markdown
from PIL import Image

max_pin_image_width = 640
max_pin_image_height = 480


with open('_build/container.html', 'r', encoding='utf-8') as html_container_file, \
    open('_build/pin.html', 'r', encoding='utf-8') as html_pin_file:
    
    html_container_template = html_container_file.read()
    pin_html_template = html_pin_file.read()
    
    for pins_dir in os.listdir('.'):
        if os.path.isdir(pins_dir) and not pins_dir.startswith('_') and not pins_dir.startswith('.'):
            html_content = '\t\t\t\t\t<h2>Pins</h2>\n' + \
                            '\t\t\t\t\t<div id="pins">\n'
    
            for pins_json_file_name in glob.glob(os.path.join(pins_dir, '*.json')):
                print("Pin file: " + pins_json_file_name)
                with open(pins_json_file_name, 'r', encoding='utf-8') as pins_json_file:
                    pins = json.load(pins_json_file)
                    for pin in pins:
                        html_content += pin_html_template \
                            .replace('{title}', pin['title']) \
                            .replace('{date}', pin['toTime']) \
                            .replace('{type}', pin['datasetId']) \
                            .replace('{image_path}', pin['title']) \
                            .replace('{world_pos_x}', str(int((pin['lng'] + 180) * 300 / 360))) \
                            .replace('{world_pos_y}', str(int((-pin['lat'] + 90) * 150 / 180))) \
                            .replace('{eob_url}}', pin['visualizationUrl']) \
                            .replace('{download_url}', pin['visualizationUrl']) \
                            .replace('{description}', markdown.markdown(pin['description']))
                
            html_content += '\t\t\t\t\t</div>\n'
        
            html = html_container_template.replace('{content}', html_content)
            html = html.replace('{layout_dir}', '../_layout')

            output_html_file = open(os.path.join(pins_dir, 'index.html'), 'w', encoding='utf-8')
            output_html_file.write(html)
            output_html_file.close() 

print("Finished building HTML for pins")
