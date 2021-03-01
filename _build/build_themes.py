import json
import re
from PIL import Image

max_theme_image_width = 240
max_theme_image_height = 200


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

    html = html.replace('{content}', html_content)
    html = html.replace('{script}', '')
    html = html.replace('{layout_dir}', '_layout')
    
    output_html_file = open('index.html', 'w', encoding='utf-8')
    output_html_file.write(html)
    output_html_file.close() 

print("Finished building HTML for themes")
