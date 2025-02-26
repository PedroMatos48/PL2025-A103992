import re

def markdown_to_html(md_text):

    def convert_headers(md_text):
        pattern = r'^(#{1,3})\s*(.+)$'
        return re.sub(pattern, lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', md_text, flags=re.MULTILINE)

    def convert_bold(md_text):
        return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', md_text)

    def convert_italic(md_text):
        return re.sub(r'\*(.+?)\*', r'<i>\1</i>', md_text)

    def convert_numbered_lists(md_text):
        pattern = r'((?:^\d+\.\s+.+(?:\n|$))+)'
    
        def replace_list(match):
            list_items = re.findall(r'^\d+\.\s+(.+)', match.group(1), flags=re.MULTILINE)
            list_html = "<ol>\n" + "".join(f"<li>{item}</li>\n" for item in list_items) + "</ol>\n"
            return list_html 

        return re.sub(pattern, replace_list, md_text, flags=re.MULTILINE)


    def convert_links(md_text):
        return re.sub(r'\[(.+?)\]\((https?:\/\/.+?)\)', r'<a href="\2">\1</a>', md_text)

    def convert_images(md_text):
        return re.sub(r'!\[(.*?)\]\((https?:\/\/.+?)\)', r'<img src="\2" alt="\1"/>', md_text)

    md_text = convert_headers(md_text)
    md_text = convert_bold(md_text)
    md_text = convert_italic(md_text)
    md_text = convert_numbered_lists(md_text)
    md_text = convert_images(md_text)
    md_text = convert_links(md_text)

    return md_text

input_filename = "input.md"
output_filename = "output.html"

with open(input_filename, "r", encoding="utf-8") as file:
    md_text = file.read()

html_text = markdown_to_html(md_text)

with open(output_filename, "w", encoding="utf-8") as file:
    file.write(html_text)

print(f"HTML saved to {output_filename}")