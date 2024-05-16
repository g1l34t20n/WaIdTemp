import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
from datetime import datetime
from pdf417 import encode, render_svg, render_image
import tkinter as tk
from tkinter import messagebox
import qrcode
import base64
import webbrowser
import random



def height_convert():

    feet_inches = entries['height'].get().strip()
    units = feet_inches.split("'-")
    if len(units) > 1:
        feetinin = int(units[0])*12
        inches = units[1].replace("\"","")
        height_inches = feetinin + int(inches)
        height = f"0{height_inches}"
    elif len(units) == 1:
        inch_unit = units[0].split()
        height_in_inches = int(inch_unit[0]) # Get input and convert to integer   # Assuming height in inches is inputted
        height = f"0{height_in_inches}"
    else:
        height = "099 in"
        print(f"error in height; Height entered as: {height} in AAMVA barcode generation.  Please check height and resubmit")
    print("Height:", height)
    return height

def load_svg(svg_file_path):
    global svg_tree
    svg_tree = ET.parse(svg_file_path)
    return svg_tree.getroot()

def load_image(label, filepath):
    img = Image.open(filepath)
    img = img.resize((150, 150), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def get_initial_value(id):
    namespaces = {
        '': 'http://www.w3.org/2000/svg',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        'xlink': 'http://www.w3.org/1999/xlink'
    }
    element = svg_tree.find(f'.//*[@id="{id}"]', namespaces)
    return element.text if element is not None and element.text is not None else ""

def inches_to_feet_inches(inches):
    feet = inches // 12
    remaining_inches = inches % 12
    return f"{feet}'-{remaining_inches}\""


# Update the SVG with new values and save as a new file
def update_svg_and_save(entries):

    city = entries["city"]
    zip_code = entries["zip_code"]
    first_name = entries["first_name"]
    middle_name = entries["middle_name"]
    address_line_2 = f"{city} WA {zip_code}"
    full_name = f"{first_name} {middle_name}"

    if city and zip_code:
        id = fields["city"]["id"]
        element = svg_tree.find(f'.//*[@id="{id}"]')
        if element is not None:
            element.text = address_line_2
    elif first_name and middle_name:
        id = fields["first_name"]["id"]
        element = svg_tree.find(f'.//*[@id="{id}"]')
        if element is not None:
            element.text = full_name
    else:
        for key, entry in entries.items():
            if key in fields:
                field = fields[key]
                id = field['id']
                element = svg_tree.find(f'.//*[@id="{id}"]')
            if element is not None:
                element.text = entry


    # Generate the filename with current date and time
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{entries['driver_license_number'].get()}.{current_time}.svg"
    new_file_path = os.path.join(script_dir, new_filename)
    svg_tree.write(new_file_path)
    print("New SVG saved:", new_filename)

def create_barcode(entries):

    # def process_weight(this_weight):
    #     my_weights = entries['weight'].get().strip()
    #     weights = this_weight.split(" ")
    #     if len(weights) == 1 and len(weights[0]) == 3:
    #         weight = weights[0]
    #     elif len(weights) > 1 or len(weights[0]) > 3:
    #         weight_string = weights[0]
    #         weight = weight_string[:3]
    # print(f"weight to encode in initial pdf417: {weight}")
    # return weight
    #
    #
    # def process_weight(weight):
    #     my_weights = (entries['weight'].get().strip())
    #     weights = split(my_weights, " ")
    #     if len(weights) == 1 and len(weights[0]) == 3:
    #         weight = weights[0]
    #     elif len(weights) > 1 or len((weights[0]) > 3):
    #         weight_string = weights[0]
    #         weight = weight_string[:3]
    #     print(f"weight to encode in ititial pdf417: {weight}")
    #     return weight

    def count_bytes(string):
        return len(string.encode('utf-8'))


    def zip_code_formatter():
        portion = split((entries['zip'].get().strip()),"-")
        if len(portion) == 2:
            compliant_zip = portion[0] + portion[1]
            zip_code = compliant_zip
        elif len(portion) == 1 and len(portion[0]) == 5:
            generalized_zip = portion[0]
            compliant_zip = f"{generalized_zip}0000"
            zip_code = compliant_zip
        elif len(portion) == 1 and len(portion[0]) == 9:
            zip_code =  portion[0]
        else:
            zip_code = "000000000"
            print(f"Error in zip-code; Please update zip and resubmit. Code entered as {zip_code}")
        print(f"Zip-Code submitted for barcode generation as: {zip_code}")
        return zip_code

    def height_convert(feet_inches):

        units = feet_inches.split("'-")
        if len(units) > 1:
            feetinin = int(units[0])*12
            inches = units[1].replace("\"","")
            height_inches = feetinin + int(inches)
            height = f"0{height_inches}"
        elif len(units) == 1:
            inch_unit = units[0].split()
            height_in_inches = int(inch_unit[0]) # Get input and convert to integer   # Assuming height in inches is inputted
            height = f"0{height_in_inches}"
        else:
            height = "099 in"
            print(f"error in height; Height entered as: {height} in AAMVA barcode generation.  Please check height and resubmit")
        print("Height:", height)
        return height

    def getsex(code):
        if code == 'M':
            return 1
        elif code == 'F':
            return 2
        else: code == 'X'
        return 9

    def date_strip(date_string):
        input_date = date_string
        numeric_date = input_date.replace("/", "")
        return numeric_date

    #aamva_data =
    first_name = entries['first_name'].get().strip()
    middle_name = entries['middle_name'].get().strip()
    last_name = entries['last_name'].get().strip()
    driver_license_number = entries['driver_license_number'].get().strip()
    audit_number = entries['audit_number'].get().strip()
    dd_number = f"{driver_license_number}{audit_number}"
    zip_code = entries['zip_code'].get().strip()
    city = entries['city'].get().strip()
    issue_date = date_strip(entries['issue_date'].get().strip())
    expiration_date = date_strip(entries['expiration_date'].get().strip())
    dob = date_strip(entries['dob'].get().strip())
    sex = getsex(entries['sex'].get().strip())
    eye_color = entries['eyes'].get().strip()
    height = height_convert(entries['height'].get().strip())
    weight = entries['weight'].get().strip()
    street_address = entries['street_address'].get().strip()
   # dd_number : update_dd_number()

    dl_file = f"DLDCANONE\x0ADCBNONE\x0ADCDNONE\x0ADBA{expiration_date}\x0ADCS{last_name}\x0ADAC{first_name}\x0ADAD{middle_name}\x0ADBD{issue_date}\x0ADBB{dob}\x0ADBC{sex}\x0ADAY{eye_color}\x0ADAU{height} in\x0ADAG{street_address}\x0ADAI{city}\x0ADAJWA\x0ADAK{zip_code}\x0ADAQ{driver_license_number}\x0ADCF{dd_number}\x0ADCGUSA\x0ADDEN\x0ADDFN\x0ADDGN\x0ADCJ{audit_number}\x0ADDAN\x0ADDB11122019\x0ADAW{weight}\x0D"

    print(dl_file)


    byte_count = count_bytes(dl_file)

    print(f'The string is {byte_count} bytes long.')

    zeroed_byte_count = f'{byte_count:04d}'

    header_file = "@\x0A\x1E\x0DANSI 636045090001DL0031{zeroed_byte_count}"
    header_file = header_file.replace("{zeroed_byte_count}", zeroed_byte_count)

    aamva_string =  header_file + dl_file

    print(aamva_string)

    codes = encode(aamva_string, columns=13, security_level=5)
    svg = render_svg(codes, ratio=4)
    svg.write('barcode.svg')
    img = render_image(codes, ratio=4)
    img.save('barcode.jpg')



def update_full_name(entries):
    first_name = entries['first_name'].get().strip()
    middle_name = entries['middle_name'].get().strip()
    full_name = f"{first_name} {middle_name}".strip()

    # Find the tspan element for the full name and update it
    namespaces = {
        '': 'http://www.w3.org/2000/svg'
    }
    full_name_element = svg_tree.find('.//*[@id="tspan91"]', namespaces)  # Adjust ID if necessary
    if full_name_element is not None:
        full_name_element.text = full_name
        print(f"Full name updated to: {full_name}")
    else:
        full_name = first_name
        print(f"First name only to appear on DL as {full_name}")
    return full_name

def update_dd_number():
    # Assuming 'entries' dictionary holds tkinter entry widgets with values loaded or input by the user
    dl_number = entries['driver_license_number'].get().strip()
    audit_number = entries['audit_number'].get().strip()
    dd_number = f"{dl_number}{audit_number}"
    namespaces = {        '': 'http://www.w3.org/2000/svg',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        'xlink': 'http://www.w3.org/1999/xlink'}  # Define namespaces if your SVG uses them
    dd_number_element = svg_tree.find('.//*[@id="tspan104"]', namespaces)
    if dd_number_element is not None:
        dd_number = dd_number_element.text
        print(f"DD number updated to: {dd_number}")
    else:
        print("DD number element not found.")

def create_form(app, fields):
    entries = {}
    # Fetch initial values for special cases
    city, zip_code = get_city_zip()
    first_name, middle_name = get_initial_name_values('tspan91')
    for field_name, details in fields.items():
        row = details['row']
        label = tk.Label(app, text=field_name.replace("_", " ").capitalize())
        label.grid(row=row, column=0)
        if field_name == 'city':
            entry = tk.Entry(app)
            entry.insert(0, city)
            entry.grid(row=row, column=1)
            entries[field_name] = entry
        elif field_name == 'zip_code':
            entry = tk.Entry(app)
            entry.insert(0, zip_code)
            entry.grid(row=row, column=1)
            entries[field_name] = entry
        elif field_name == 'first_name':
            entry = tk.Entry(app)
            entry.insert(0, first_name)
            entry.grid(row=row, column=1)
            entries[field_name] = entry
        elif field_name == "middle_name":
            entry =tk.Entry(app)
            entry.insert(0, middle_name)
            entry.grid(row=row, column=1)
            entries[field_name] = entry
        else:
            entry = tk.Entry(app)
            initial_value = get_initial_value(details['id'])
            entry.insert(0, initial_value)
            entry.grid(row=row, column=1)
            entries[field_name] = entry
    return entries

def get_city_zip():
    element = svg_tree.find('.//*[@id="tspan94"]')
    if element is not None and element.text:
        parts = element.text.split(" WA ")
        city = parts[0] if parts else ""
        if len(parts) > 1 and len(parts[1]) == 10:
            zip_code = parts[1]
        elif len(parts[1]) == 5:
            zip_code = f"{parts[1]}-0000"
        elif len(parts[1]) == 9:
            input_string = parts[1]
            zip_code = input_string[:5] + "-" + input_string[5:]
        else:
            print("Problem with zip format")
            zip_code = ""
        print(f"city is: {city} and zip is: {zip_code}")
        return city, zip_code
    else:
        print("Problem getting initial city and zip code; Check address line 2 or input boxes")
        return "", ""

def get_initial_name_values(id):
    element = svg_tree.find(f'.//*[@id="{id}"]')
    if element is not None and element.text:
        names = element.text.split(" ", 1)
        return names[0], names[1] if len(names) > 1 else ''
    else:
        return "", ""

def on_submit(entries):
    update_full_name(entries)  # Update the full name in the SVG
   # height_in_inches = int(entries['height'].get())  # Get input and convert to integer   # Assuming height in inches is inputted
    #formatted_height = inches_to_feet_inches(height_in_inches)
   # print("Formatted Height:", formatted_height)
    height = height_convert(entries['height'].get().strip())
   # height_convert(entered_height)
    update_dd_number()
    create_barcode(entries)
    update_svg_and_save(entries)  # Update other data as needed and save the new SVG file
    print("Data submitted and SVG updated.")



app = tk.Tk()
app.title("WA Driver License Generator")
script_dir = os.path.dirname(__file__)
svg_file_path = os.path.join(script_dir, 'WaIdTemp.svg')
load_svg(svg_file_path)

fields = {
    "driver_license_number": {"id": "tspan25", "type": "text", "row": 1},
    "issue_date": {"id": "tspan103", "type": "text", "row": 2},
    "expiration_date": {"id": "tspan100", "type": "text", "row": 3},
    "audit_number": {"id": "tspan88", "type": "text", "row": 4},
    "first_name": {"id": "tspan91", "type": "text", "row": 5},
    "middle_name": {"id": "tspan91", "type": "text", "row": 6},
    "last_name": {"id": "tspan90", "type": "text", "row": 7},
    "dob": {"id": "tspan92", "type": "text", "row": 8},
    "street_address": {"id": "tspan93", "type": "text", "row": 9},
    "city": {"id": "tspan94", "type": "text", "row": 10},
    "zip_code": {"id": "tspan94", "type": "text", "row": 11},
    "sex": {"id": "tspan95", "type": "text", "row": 12},
    "eyes": {"id": "tspan97", "type": "text", "row": 13},
    "weight": {"id": "tspan98", "type": "text", "row": 14},
    "height": {"id": "tspan96", "type": "text", "row": 15},
    "back_data_number_21": {"id": "tspan26" , "type": "text", "row": 16},
  #  "back_dob": {"id": "tspan86", "type": "text", "row":""}
}



entries = create_form(app, fields)
submit_btn = tk.Button(app, text="Create Your License", command=lambda: on_submit(entries))
submit_btn.grid(row=16, column=1)
create_barcode(entries)

#images = {
    #    "barcode_image_photo": {"id": "imagexxXXxx", "size": 'xxXXxx", "opaticy": xxXXxx, "location": "XXyyZZ", image_file_path:barcode.svg}
    #    "driver_license_photo": {"id": "image". "size":  "", "opaticy": "", "location": "", "image_file_path":cardholder_photo.jpg}
#        "driver_license_small_photo":  {"id": "image". "size":  "", "opaticy": "", "location": "", "image_file_path":cardholder_photo.jpg}
#        "barcode_128":  {"id": "image". "size":  "", "opaticy": "", "location": "", "image_file_path":cardholder_photo.jpg}
#}

barcode_image_photo_label = tk.Label(app)
barcode_image_photo_label.grid(row=17, column=1, rowspan=3)
update_barcode_image_photo_button = tk.Button(app, text="update barcode",
                                            command=lambda: load_image(barcode_image_photo_label, 'barcode.jpg'))
update_barcode_image_photo_button.grid(row=21, column=1)
# Image fields setup

# Driver's License Photo
driver_license_photo_label = tk.Label(app)
driver_license_photo_label.grid(row=1, column=2, rowspan=5)
load_driver_license_photo_button = tk.Button(app, text="Load Driver's License Photo",
                                             command=lambda: load_image(driver_license_photo_label, filedialog.askopenfilename()))
load_driver_license_photo_button.grid(row=6, column=2)

# Signature
signature_photo_label = tk.Label(app)
signature_photo_label.grid(row=7, column=2, rowspan=1)
load_signature_photo_button = tk.Button(app, text="Load Signature Photo",
                                        command=lambda: load_image(signature_photo_label, filedialog.askopenfilename()))
load_signature_photo_button.grid(row=11, column=2)

#error_note = tk.Label(app, text="Inches must be Input or it will Crash upon Creation!")
#rror_note.grid(row=15, column=2)

app.mainloop()