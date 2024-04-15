import json

def json_to_html(json_file_path, html_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Start building HTML content
    html_content = '<AAMVA>\n'
    user = data['user']
    head = data['head']
    subfiles = data['subfiles']

    # Add user data
    html_content += '<user>\n'
    for key, value in user.items():
        html_content += f'    <{key} e="{key[:3].upper()}">{value}</{key}>\n'
    html_content += '</user>\n'

    # Add header data
    html_content += '<head>\n'
    for key, value in head.items():
        html_content += f'    <{key} name="{key}">{value}</{key}>\n'
    html_content += '</head>\n'

    # Add subfiles
    for subfile in subfiles:
        html_content += f'<subfile designator="{subfile["designator"]}">\n'
        for element in subfile["elements"]:
            html_content += f'    <element id="{element["id"]}" name="{element["name"]}">{element["value"]}</element>\n'
        html_content += '</subfile>\n'

    html_content += '</AAMVA>'

    # Save to HTML file
    with open(html_file_path, 'w') as file:
        file.write(html_content)

# Usage
json_file_path = 'C:\\Users\\Administrator\\Documents\\WaIdTemp\\WaIdTempChanges.json'
html_file_path = 'C:\\Users\\Administrator\\Documents\\WaIdTemp\\output.html'
json_to_html(json_file_path, html_file_path)
