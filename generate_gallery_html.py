import os
import sys
import functools


supported_types = ['jpg', 'png']

program_dir = os.path.dirname(os.path.realpath(__file__))
head_template_path = os.path.join(program_dir, 'index.html.head')
assert os.path.exists(head_template_path), "Path not exists: %s" % (head_template_path)
with open(head_template_path) as f:
    head_template = ''.join(f.readlines())


def compare_str(str1, str2):
    if len(str1) < len(str2):
        return -1
    elif len(str1) > len(str2):
        return 1
    elif str1 < str2:
        return -1
    elif str1 == str2:
        return 0
    elif str1 > str2:
        return 1


def get_img_code_block(img_path):
    img_src = '<img src="' + img_path + '" alt="None">\n'
    desc = '<div class="desc">' + img_path + '</div>\n'

    code = '<div class="gallery">\n'
    code += img_src
    code += desc
    code += '</div>\n'
    return code 


def generate_index_html(work_dir, max_number=10000):
    assert os.path.exists(work_dir), "Path not exists: %s" % (work_dir)
    
    file_list = os.listdir(work_dir)
    file_list = sorted(file_list, key=functools.cmp_to_key(compare_str))
    
    ct = 0
    content = head_template + "<body>\n"
    for item in file_list:
        # recursively process subdirectories
        if os.path.isdir(os.path.join(work_dir, item)):
            generate_index_html(os.path.join(work_dir, item))

        if item.split('.')[-1] in supported_types:
            content += get_img_code_block(item)
            ct += 1

            if ct > max_number:
                break
    content += "</body>\n</html>"

    if ct > 0:
        output_path = os.path.join(work_dir, "index.html")
        with open(output_path, 'w') as f:
            f.writelines(content)
        print(f'Found {ct} images in : {output_path}.')
    else:
        print(f'Found NO images in : {output_path}.')
    return ct


if __name__ == '__main__':

    work_dir = sys.argv[1]
    assert os.path.exists(work_dir)

    generate_index_html(work_dir)
    
