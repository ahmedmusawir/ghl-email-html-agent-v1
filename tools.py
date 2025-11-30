from bs4 import BeautifulSoup
import re
import os
import json
import sys

def apply_style_edit(html_content: str, selector: str, css_property: str, css_value: str) -> str:
    """
    Parses HTML, finds elements matching the selector, and updates a specific CSS property 
    in their inline style attribute without overwriting other styles.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(selector)

    for element in elements:
        current_style = element.get('style', '')
        style_dict = {}
        
        # Parse existing styles into a dictionary
        if current_style:
            # Split by semicolon, filter empty strings
            styles = [s.strip() for s in current_style.split(';') if s.strip()]
            for style_pair in styles:
                if ':' in style_pair:
                    key, value = style_pair.split(':', 1)
                    style_dict[key.strip().lower()] = value.strip()
        
        # Update or add the new property
        style_dict[css_property.strip().lower()] = css_value.strip()
        
        # Reconstruct the style string
        new_style_str = '; '.join([f"{k}: {v}" for k, v in style_dict.items()])
        if new_style_str:
            new_style_str += ';' # Add trailing semicolon for good measure
            
        element['style'] = new_style_str

    return str(soup)

def update_text_content(html_content: str, selector: str, new_text: str) -> str:
    """
    Finds elements matching the selector and replaces their text content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(selector)
    
    for element in elements:
        element.string = new_text
        
    return str(soup)

def update_inner_html(html_content: str, selector: str, new_html: str) -> str:
    """
    Finds elements matching the selector and replaces their inner HTML content.
    This allows for rich text updates (e.g. adding <span> tags).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(selector)
    
    for element in elements:
        # Clear existing content
        element.clear()
        
        # Parse new HTML fragment
        new_soup = BeautifulSoup(new_html, 'html.parser')
        
        # Extract contents and append to the element
        if new_soup.body:
            tags_to_insert = list(new_soup.body.contents)
        else:
            tags_to_insert = list(new_soup.contents)
            
        for tag in tags_to_insert:
            element.append(tag)
            
    return str(soup)

def insert_element_relative(html_content: str, target_selector: str, new_html: str, position: str = 'after') -> str:
    """
    Parses new_html and inserts it relative to the element matching target_selector.
    position: 'before', 'after', 'inside_start', 'inside_end'
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    target_elements = soup.select(target_selector)
    
    if not target_elements:
        return f"ERROR: No element found matching selector '{target_selector}'"
        
    for target in target_elements:
        # Parse the new element specifically for this insertion
        temp_soup = BeautifulSoup(new_html, 'html.parser')
        
        # Extract contents
        if temp_soup.body:
            tags_to_insert = list(temp_soup.body.contents)
        else:
            tags_to_insert = list(temp_soup.contents)
            
        # Perform insertion based on position
        if position == 'before':
            for tag in tags_to_insert:
                target.insert_before(tag)
        elif position == 'after':
            for tag in reversed(tags_to_insert):
                target.insert_after(tag)
        elif position == 'inside_start':
            for tag in reversed(tags_to_insert):
                target.insert(0, tag)
        elif position == 'inside_end':
            for tag in tags_to_insert:
                target.append(tag)
        else:
            # Default to append (inside_end) if unknown position
             for tag in tags_to_insert:
                target.append(tag)
                
    return str(soup)

def remove_element(html_content: str, selector: str) -> str:
    """
    Finds all elements matching the selector and removes them from the HTML tree.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select(selector)
    
    if not elements:
        return "ERROR: No elements found to remove."
        
    for element in elements:
        element.decompose()
        
    return str(soup)

if __name__ == "__main__":
    # JSON File Test Harness
    
    if len(sys.argv) < 2:
        print("Usage: python tools.py <path_to_json_file>")
        exit(1)

    json_path = sys.argv[1]
    sample_path = os.path.join("data", "sample_ghl.html")
    output_path = "output.html"
    
    try:
        if not os.path.exists(json_path):
            print(f"Error: JSON file '{json_path}' not found.")
            exit(1)
            
        if not os.path.exists(sample_path):
            print(f"Error: Sample HTML '{sample_path}' not found.")
            exit(1)

        # Read JSON Payload
        with open(json_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
        function_name = payload.get("function_name")
        args = payload.get("args", {})
        
        if not function_name or function_name not in globals():
            print(f"Error: Function '{function_name}' not found or invalid.")
            exit(1)

        # Read HTML Content
        with open(sample_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Execute Function
        print(f"Executing {function_name} with args: {args}...")
        func = globals()[function_name]
        modified_html = func(html_content, **args)
        
        # Save Result
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(modified_html)
            
        print(f"✅ Executed {function_name}. Result saved to {output_path}")

    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{json_path}'.")
    except Exception as e:
        print(f"Critical Error: {e}")
