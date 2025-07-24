import os
import shutil
import sys
from common import *

def copy_directory(src, dst):
    if not os.path.exists(src):
        raise Exception(f"Directory {src} does not exist.")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    if os.path.exists(src):
        for fname in os.listdir(src):
            src_path = os.path.join(src, fname)
            dst_path = os.path.join(dst, fname)
            if os.path.isdir(src_path):
                copy_directory(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path) or not os.path.isfile(from_path):
        raise Exception(f"Source file {from_path} does not exist.")
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        raise Exception(f"Template file {template_path} does not exist.")
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        content = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    page_content = markdown_to_htmlnode(content).to_html()
    full_page = template.replace("{{ Content }}", page_content).replace("{{ Title }}", extract_title(content))
    full_page = full_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    full_page = full_page.replace('href=/', f'href={basepath}').replace('src=/', f'src={basepath}')
    
    with open(dest_path, 'w') as f:
        f.write(full_page)

def generate_page_recursive(from_dir_path, template_path, dest_dir_path, basepath):
    if not os.path.exists(from_dir_path) or not os.path.isdir(from_dir_path):
        raise Exception(f"Source directory {from_dir_path} does not exist.")
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        raise Exception(f"Template file {template_path} does not exist.")
    
    for file in os.listdir(from_dir_path):
        file_path = os.path.join(from_dir_path, file)
        if os.path.isdir(file_path):
            new_dest_dir = os.path.join(dest_dir_path, file)
            generate_page_recursive(file_path, template_path, new_dest_dir, basepath)
        elif file.endswith(".md"):
            dest_file_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
            generate_page(file_path, template_path, dest_file_path, basepath)

def generate_static_site(from_path, template_path, dest_path, basepath):
    static = "/home/deck/Documents/workspace/github/static-site-generator/static"
    public = "/home/deck/Documents/workspace/github/static-site-generator/docs"
    copy_directory(static, public)
    generate_page_recursive(from_path, template_path, dest_path, basepath)

def main():
    basepath = sys.argv[1]
    if not basepath:
        basepath = "/"

    generate_static_site(
        "/home/deck/Documents/workspace/github/static-site-generator/content",
        "/home/deck/Documents/workspace/github/static-site-generator/template.html",
        "/home/deck/Documents/workspace/github/static-site-generator/docs",
        basepath
    )

main()