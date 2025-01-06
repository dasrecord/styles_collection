import re

def read_css_file(filename="custom.css"):
    try:
        with open(filename, 'r') as file:
            css_content = file.read()
        return css_content
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def generate_swatches_html(css_content):
    # Regular expressions to find CSS variables and group names
    var_regex = re.compile(r'--([^:]+):\s*([^;]+);')
    group_regex = re.compile(r'/\*\s*([^*]+)\s*\*/')
    groups = []
    current_group = None

    # Extract variables and their values
    for line in css_content.splitlines():
        group_match = group_regex.search(line)
        var_match = var_regex.search(line)
        if group_match:
            # Found a group name
            current_group = group_match.group(1).strip()
            groups.append({'name': current_group, 'variables': []})
        elif var_match and current_group:
            # Found a CSS variable
            var_name = var_match.group(1).strip()
            var_value = var_match.group(2).strip()
            groups[-1]['variables'].append({'name': f'--{var_name}', 'value': var_value})

    # Generate HTML
    html = ''
    for group in groups:
        html += f'<div class="group">\n  {group["name"]}\n  <div class="swatches">'
        for variable in group['variables']:
            html += f'\n    <div class="swatch">\n      <div style="background-color: {variable["value"]}"></div>\n      <span>{variable["name"]}</span>\n    </div>'
        html += '\n  </div>\n</div>'
    return html

def replace_body_content(html_file_path, new_content):
    try:
        with open(html_file_path, 'r') as file:
            html_content = file.read()
        
        body_regex = re.compile(r'(<main[^>]*>)([\s\S]*?)(</main>)', re.IGNORECASE)
        updated_html_content = body_regex.sub(rf'\1\n{new_content}\n\3', html_content)
        
        with open(html_file_path, 'w') as file:
            file.write(updated_html_content)
    except FileNotFoundError:
        print(f"Error: {html_file_path} not found")
    except Exception as e:
        print(f"Error updating file: {e}")

# Read the CSS file
css_content = read_css_file()
if css_content:
    # Generate swatches HTML
    swatches_html = generate_swatches_html(css_content)
    
    # Replace body content in index.html
    html_file_path = "index.html"
    replace_body_content(html_file_path, swatches_html)
    
    print('Swatches HTML generated and inserted into index.html')