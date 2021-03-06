## Welcome!

Welcome to the pin library, where anyone can browse and share satellite imagery of interesting locations and events of the Earth! There are several themes available, each holding many pins with images, descriptions and locations. We're hoping it can become a repository of remote sensing imagery, useful to any enthusiast, teacher, student or researcher. Don't forget to click on the EO Browser link for the pin that picks your interest, to explore it yourself! 

## 1. Contribute to Pin Library

So you want to contribute to the wonderful world of satellite imagery? Just follow these instructions and you'll be started in no time!

The pins are exported from [EO Browser](https://apps.sentinel-hub.com/eo-browser/), where the satellite, date, location, visualization and description are all set, and finally uploaded to the Pin Library using git. 
If you're not familiar with how to configure and export the pins from EO Browser, start with chapter 2, and return to chapter 1 when you have your pins exported. 

The guide below will explain how to contribute the whole new theme of pins, explaining how Pin Library is structured. If you would like to contribute to an existing theme, read the chapter 1.4 and refer to the reffered chapters as needed. 

**Basic information**

To contribute content to pin library, you need the following: 
- A JSON file with EO Browser pins (check section 2)
- Installed git and the Pin Library repository cloned (see [this guide](https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners) to learn how to use git)
- Images for each pin downloaded (you can use the EO Browser download feature, or create a screenshot using Greenshot or a similar application). 

All you need to do to add a new theme is to complete the following steps, which are explained in detail below: 

1. Export the pin JSON from EO Browser
2. Clone the repository
3. Create a new folder for your theme, add a subfolder called `fig` for images and copy in the JSON file with the same name as the theme folder
4. Replace the names of your images with the unique pin IDs
5. Add a theme thumbnail image
6. Create a pull request

Additionally, you can optionally group your pins and add high resolution URLs. 

When you complete all the required steps and create a pull request, the INDEX file, which will hold the actual content of the Pin Library theme website, will be generated automatically. It will be parsed based on your JSON file, so you won't need to add any additional files, save from the ones listed above. 

When you commit your changes, our team will check your contribution in the shortest possible time. 

**Please read the chapters below carefully.** 


### 1.1 Examine the JSON file

The image below displays the structure of the JSON file exported from EO Browser. 
The black rectangle shows the structure of a single pin; each pin is included in curly brackets `{}`, and all pins are listed inside a large array `[]` and separated by commas.

- `_id:` - underlined with green: A unique pin ID, given to each pin on export. You will copy the value of this field to replace your image names. See chapter 1.3 for more information. SHOULD NOT BE CHANGED.
- `title` - underlined with orange: Pin title, as displayed in EO Browser and Pin Library. Should already be set in EO Browser, but can be changed later. Check chapter 1.2 for more information
- `group` - underlined with blue: Optional parameter. You can use it to group pins together to be displayed as one group on the pin library. By default set to `null` - if desired, the user needs to update it after export. See chapter 1.5 for more information.
- `highResImageUrl` - underlined with purple: Optional parameter. If you have a high resolution image uploaded on Flickr or other similar website, you can add the link here. By default set to `null` - if desired, the user needs to update it after export. See chapter 1.6 for more information.
- `description` - underlined with red: The description you added in EO Browser. Should already be set in EO Browser, but can be changed later. Check chapter 2.2 for more information.

![json](/_imgs/Readme/json.png)

**Note that the only parameters you can edit are `title`, `description`, `group` and `highResImageUrl`. Changing any other existing parameter could cause your pin to not work!**

### 1.2 Set up folders 

- In your local pin library repository, create a new folder with the name of your theme. Separate the words in the name using the `_` sign.
To demonstrate, we have added a folder called "Clouds_and_Hurricanes". 

![folder1](/_imgs/Readme/theme.png)

- Copy your JSON file into this folder. Rename the JSON file so that it matches the name of your theme folder. For example, if the theme folder is named "Clouds_and_Hurricanes", the JSON file should also be named "Clouds_and_Hurricanes". Note that this is the name that will be displayed on the top of your theme in the Pin Library. If you would like to note your name, you simply add your name to the theme name like so: "themeName_by_yourName" (e.g. "Clouds_and_Hurricanes_by_Monja").

- In the same folder, create another folder called `fig` (should be lowercase). 

![folder2](/_imgs/Readme/folder2.png)

### 1.3 Images

**Pin images**

- Paste all your pin images corresponding to the same theme, into your newly created `fig` folder. 
- Next, replace the name of each image with the unique ID from the JSON file for the corresponding pin, like in the image below. From each pin, grab the value of the `_id` parameter. For example, from the line `"_id": "119aea85-e6a8-4a75-a3f6-9bfab4519ea2-pin"`, grab only the value, which in this case equals to `119aea85-e6a8-4a75-a3f6-9bfab4519ea2-pin` and paste it into the image name like so: `119aea85-e6a8-4a75-a3f6-9bfab4519ea2-pin.png`.

![arrow](/_imgs/Readme/image_rename.png)

**Theme thumbnail image**

- Next, you will need to add an image to represent your theme. As you can see on the image below, each theme has its own thumbnail, which is usually one of the pins, that best represents it. 

![first_page](/_imgs/Readme/lib_themes.png)

- To add a thumbnail for your new theme, just add a desired image into the folder `\_themeimgs` and **make sure the image is named exactly the same as your theme folder and JSON file**.

![thumbnail](/_imgs/Readme/theme_imgs.png)

### 1.6 Contribute to existing themes

- To add a new pin to the existing theme, export the particular pin from EO Browser and copy it from the exported JSON file (only the pin content, which is between the `{}` symbols) to the JSON file of the theme (located in the theme folder). Make sure that all the pins have a comma at the end, except the last one, and that they are all included in a larger array. Don't forget to add an image for the pin.  Refer to chapter 1.1 for the JSON structure, chapter 1.2 for folder setup, chapter 1.3 for images and chapter 2 for exporting pins from EO Browser. 
- Don't forget to add an image to the pin, if you're adding a new one. Refer to the chapter 1.2. 
- To update an image, replace the image with another one, and make sure the name of the image stays the same, to keep the connection to the pin. The images are located in the theme folders -> subfolder `fig`. Refer to the chapter 1.2 for folder structure and 1.3 for images. 
- To change a theme thumbnail, replace an image and leave the name as it was, in the `\_themeimgs` folder. Refer to the chapter 1.3, Theme thumbnail image. 
- To edit a description or title, you need to edit it directly in the JSON file. Refer to chapter 1.1 for the JSON structure and 2.2 for the Markdown guide. 
- To connect several pins into a group, match the `group` parameter for each pin in the same group. Refer to chapter 1.1 for the JSON structure and 1.5 for the grouping guide. 
- To add a high resolution link, add an URL to the `highResImageUrl` parameter. Refer to chapter 1.1 for the JSON structure and 1.6 for the high resolution URL. 
- Check the previous chapters for more information.

### 1.5 Groups (OPTIONAL)

If you leave your setup as it is, each pin will be a separate entity in your theme, such as with the Agriculture theme. 

![Agriculture](/_imgs/Readme/agriculture_pin.png)

If you would like to group pins by location, event or content, like for example in the Wildfires theme, where you can browse between several pins under the same category, you can do so using the optional `group` parameter in the JSON file. 

![Agriculture](/_imgs/Readme/croatia_pins.png)

You will have to open your JSON file and make sure that the pins you want grouped, have the same `group` value. The value can be anything - it can be a common theme, such as for example "Rice Fields", or it can be a number (e.g. 1). In the pin library, the group name will not be displayed - it will only be used to connect the pins together. It's crucial, that the same value is used for all the pins belonging to the same group. 

By default, group value is set to `null`. You will have to replace `null` with `"groupValue"`, where groupValue is anything you want to name your group. Don't forget to add the quotation marks around it as well, and be careful not to accidentally delete the comma after the parameter. The JSON structure must stay like this: 

`"group":"Value",`

Note that you can also add a non-image element to the group, such as a photograph, a timelapse or a legend, by adding JSON content outside of the pin and adding the group parameter with the same value. (recommended only for experienced users). 

### 1.6 High resolution links (OPTIONAL)

You can add a URL link to a high resolution image of the pin, if available, to the `"highResImageUrl"` parameter. In the Pin Library, you can see that some pins have the button "High-res download" available under the "Open in EO Browser" button. These are the pins, which have this optional parameter set. 
By default, this value is set to `null`. You will have to replace `null` with `"URL"`, where URL is the link to your high resolution image of the pin. Don't forget to add the quotation marks around it as well, and be careful not to accidentally delete the comma after the parameter. The JSON structure must stay like this: 

`"highResImageUrl":"www.link.com",`

## 2. Export pins from EO Browser

The pins you will upload to Pin Library need to be configured in [EO Browser](https://apps.sentinel-hub.com/eo-browser/). If you don't know how to use EO Browser, check out [this tutorial](https://www.sentinel-hub.com/explore/eobrowser/).
 
### 2.1 Save your pins

Save your chosen location as pin, by clicking on the pin icon in the top menu on the left (as highlighted with a red rectancle). 

![save_pin](/_imgs/Readme/location.png))

### 2.2. Edit your pins

Open the Pin tab on top (blue rectangle on the image above), to display all your pins. 

Edit each pin to change its name and add a description in [Markdown](https://learnxinyminutes.com/docs/markdown/). Click on the pen icon on the right to change the name, and confirm it by clicking the green check mark on the right. Then expand the arrows on bottom right, to open the description panel. Use Markdown to add a description and confirm it by clicking the green check mark on bottom right. 

![edit_pin](/_imgs/Readme/pin.png)

_**Mini Markdown guide:**_
- Headings are made using #. More #, smaller heading. For example: `# My Heading`, or `## My smaller heading`. Note that you need a space after the #. 
- Lists are made simply using - sign before each line. 
- To add links, write `[Text](www.url.com)`, which will display what you write in square brackets as clickable text with a link. 
- To add images, commit them to a folder and then access it with the following structure: `![ImageName](/imgFolder/imgName.png)`. Note that you can't do this in EO Browser directly. 
- Use ** before and after text to make it bold (e.g. `**Text**`) and use _ before and after text to make it italic (eg. `_Text_`)
- Use `<br/>` to make page breaks

You can delete the pins by clicking the trash can icon on the left, and you can organize the sequence of pins by clicking the drag icon (dots on the left) and rearranging them by dragging one on top of the other. The sequence of the pins in EO Browser will be the same as the sequence of pins in the Pin library, unless manually editing a JSON file. 

![delete_rearrange_pins](/_imgs/Readme/delete.png)

### 2.3. Export pins

Export pins from EO Browser by clicking the Export button. Note that all the pins in your list will be added - make sure to remove those you don't want included before hand (or remove them manually from the JSON file later).

![export_pins](/_imgs/Readme/export.png)


