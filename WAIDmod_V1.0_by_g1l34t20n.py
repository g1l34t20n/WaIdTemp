import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
from datetime import datetime

def load_svg(svg_file_path):
    global svg_tree
    svg_tree = ET.parse(svg_file_path)
    return svg_tree.getroot()

def load_image(label, filepath):
    img = Image.open(filepath)
    img = img.resize((150, 150), Image.ANTIALIAS)
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
    for key, entry in entries.items():
        id = fields[key]['id']  # Get the ID for the field
        element = svg_tree.find(f'.//*[@id="{id}"]')
        if element is not None:
            element.text = entry.get()

    # Generate the filename with current date and time
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{entries['driver_license_number'].get()}.{current_time}.svg"
    new_file_path = os.path.join(script_dir, new_filename)
    svg_tree.write(new_file_path)
    print("New SVG saved:", new_filename)



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
        print("Full name updated to:", full_name)
    else:
        print("Full name element not found.")


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
        dd_number_element.text = dd_number
        print("DD number updated to:", dd_number)
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
        elif field_name == 'first_name' or field_name == 'middle_name':
            entry = tk.Entry(app)
            entry.insert(0, first_name if field_name == 'first_name' else middle_name)
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
        zip_code = parts[1] if len(parts) > 1 else ""
        return city, zip_code
    return "", ""

def get_initial_name_values(id):
    element = svg_tree.find(f'.//*[@id="{id}"]')
    if element is not None and element.text:
        names = element.text.split()
        return names[0], ' '.join(names[1:]) if len(names) > 1 else ''
    return "", ""

def on_submit(entries):
    update_full_name(entries)  # Update the full name in the SVG
    height_in_inches = int(entries['height'].get())  # Get input and convert to integer   # Assuming height in inches is inputted
    formatted_height = inches_to_feet_inches(height_in_inches)
    print("Formatted Height:", formatted_height)
    update_dd_number()
    update_svg_and_save(entries)  # Update other data as needed and save the new SVG file
    print("Data submitted and SVG updated.")


app = tk.Tk()
app.title("WA Driver License Generator")
script_dir = os.path.dirname(__file__)
svg_file_path = os.path.join(script_dir, 'data', 'WaIdTemp.svg')
load_svg(svg_file_path)

fields = {
    "driver_license_number": {"id": "tspan19", "type": "text", "row": 1},
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
    "height": {"id": "tspan96", "type": "text", "row": 15}
}

entries = create_form(app, fields)
submit_btn = tk.Button(app, text="Create Your License", command=lambda: on_submit(entries))
submit_btn.grid(row=16, column=1)

# Image fields setup

# Driver's License Photo
#driver_license_photo_label = tk.Label(app)
#driver_license_photo_label.grid(row=1, column=2, rowspan=4)
#load_driver_license_photo_button = tk.Button(app, text="Load Driver's License Photo",
 #                                            command=lambda: load_image(driver_license_photo_label, filedialog.askopenfilename()))
#load_driver_license_photo_button.grid(row=5, column=2)

# Signature
#signature_photo_label = tk.Label(app)
#signature_photo_label.grid(row=7, column=2, rowspan=4)
#load_signature_photo_button = tk.Button(app, text="Load Signature Photo",
 #                                       command=lambda: load_image(signature_photo_label, filedialog.askopenfilename()))
#load_signature_photo_button.grid(row=11, column=2)

#error_note = tk.Label(app, text="Inches must be Input or it will Crash upon Creation!")
#rror_note.grid(row=15, column=2)

app.mainloop()
