"""
Amend upstream patch format for anolis cloud kernel
--------------------------
Author: Aubrey Li
"""

import os
import sys
import re
import getopt

anbz_str  = 'ANBZ: #16164'
sig_str   = 'Backport Auto-tune per-CPU pageset size.'
amend_str = '[ Aubrey Li: amend commit log ]'
sob_str   = 'Signed-off-by: Aubrey Li <aubrey.li@linux.intel.com>'

def extract_commit_id(patch_text):
    lines = patch_text.split('\n')
    commit_id_match = re.match(r'From ([0-9a-f]{40}) ', lines[0])
    
    if not commit_id_match:
        raise ValueError("Invalid patch format: Commit ID not found")
    
    return commit_id_match.group(1)

def extract_subject_content(patch_text):
    lines = patch_text.split('\n')
    subject_start_idx = next((i for i, line in enumerate(lines) if line.startswith('Subject:')), None)
    if subject_start_idx is None:
        raise ValueError("Invalid patch format: Subject line not found")

    subject_line = lines[subject_start_idx][len('Subject: '):].strip()

    if (lines[subject_start_idx + 1].strip() != ''):
        full_subject = subject_line + ' ' + lines[subject_start_idx + 1].strip()
    else:
        full_subject = subject_line
    
    subject_parts = full_subject.split()
    if len(subject_parts) < 2:
        raise ValueError("Invalid patch format: Subject line too short")
    
    return " ".join(subject_parts[2:])
    
def insert_anbz_line(patch_text):
    lines = patch_text.split('\n')

    subject_start_idx = next((i for i, line in enumerate(lines) if line.startswith('Subject:')), None)
    if subject_start_idx is None:
        raise ValueError("Invalid patch format: Subject line not found")
    
    insert_index = subject_start_idx + 1
    while insert_index < len(lines):
        if lines[insert_index].strip() == '':
            break
        insert_index += 1
    
    if insert_index >= len(lines):
        raise ValueError("Invalid patch format: blank line not found")
    else:
        lines.insert(insert_index, anbz_str)
        lines.insert(insert_index, '')
    
    return '\n'.join(lines)

def insert_commit_line(patch_text):
    commit_id = extract_commit_id(patch_text)
    lines = patch_text.split('\n')

    subject_start_idx = next((i for i, line in enumerate(lines) if line.startswith('Subject:')), None)
    if subject_start_idx is None:
        raise ValueError("Invalid patch format: Subject line not found")
    
    insert_index = subject_start_idx + 1
    while insert_index < len(lines):
        if lines[insert_index].strip() == '':
            break
        insert_index += 1
    
    if insert_index >= len(lines):
        raise ValueError("Invalid patch format: blank line not found")
    else:
        lines.insert(insert_index, f'commit {commit_id} upstream.')
        lines.insert(insert_index, '')
    
    return '\n'.join(lines)
    
def insert_intel_sig(patch_text):
    commit_id = extract_commit_id(patch_text)
    subject_content = extract_subject_content(patch_text)
    lines = patch_text.split('\n')

    dash_idx = next((i for i, line in enumerate(lines) if line.strip() == '---'), None)
    if dash_idx is None:
        raise ValueError("Invalid patch format: blank line not found")
    
    insert_index = dash_idx - 1
    while insert_index >= 0:
        if lines[insert_index].strip() == '':
            break
        insert_index -= 1
    
    if insert_index < 0:
        raise ValueError("Invalid patch format: blank line not found")
    else:
        lines.insert(insert_index, sig_str)
        lines.insert(insert_index, f'Intel-SIG: commit {commit_id[:12]} {subject_content}.')
        lines.insert(insert_index, '')
    
    return '\n'.join(lines)

def insert_signature(patch_text):
    lines = patch_text.split('\n')

    insert_index = 0
    while insert_index < len(lines):
        if lines[insert_index].strip() == '---':
            break
        insert_index += 1

    if insert_index >= len(lines):
        raise ValueError("Invalid patch format: blank line not found")
    else:
        lines.insert(insert_index, sob_str)
        lines.insert(insert_index, amend_str)
    return '\n'.join(lines)

def process_patch(filename):
    with open(filename, "r", encoding="utf-8") as f:
        patch_text = f.read()
    
    patch_text = insert_commit_line(patch_text)
    patch_text = insert_anbz_line(patch_text)
    patch_text = insert_intel_sig(patch_text)
    patch_text = insert_signature(patch_text)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(patch_text)

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".patch"):  # Ensure we only process .patch files
            file_path = os.path.join(directory, filename)
            process_patch(file_path)

def print_help():
    help_message = """
    Please specify a patch file using -p or --patch, or a directory using -d or --directory.
    """
    print(help_message)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:d:", ["help", "patch=", "directory="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    patch_file = None
    directory = None

    if not opts or ('-h' in dict(opts) or '--help' in dict(opts)):
        print_help()
        sys.exit(0)

    for opt, arg in opts:
        if opt in ("-p", "--patch"):
            patch_file = arg
            process_patch(patch_file)
        elif opt in ("-d", "--directory"):
            directory = arg
            process_directory(directory)
        else:
            print_help()

if __name__ == "__main__":
    main()
