#!/usr/bin/env python3
"""
Subject: Amend upstream patch format for downstream community backport
Author:  Aubrey Li
Copyright: (C) 2025 Intel Corporation.
License:
Description:

    - Export the patch files for backporting from the upstream Linux kernel repo

        $git format-patch 1f4f7f0f8845..362d37a106dd
        0001-mm-pcp-avoid-to-drain-PCP-when-process-exit.patch
        0002-cacheinfo-calculate-size-of-per-CPU-data-cache-slice.patch
        0003-mm-pcp-reduce-lock-contention-for-draining-high-orde.patch

    - Move the patch files to a directory and run amend_patch.py script

        $python amend_patch.py -c anolis -p ./patches/0001-mm-pcp-avoid-to-drain-PCP-when-process-exit.patch

      Or
        $python amend_patch.py -c oc -p ./patches/0002-cacheinfo-calculate-size-of-per-CPU-data-cache-slice.patch

      Or
        $python amend_patch.py -c euler -p ./patches/0003-mm-pcp-reduce-lock-contention-for-draining-high-orde.patch

      Or
        $python amend_patch.py -c baseline -d ./patches

    - Start backporting
"""

import os
import sys
import re
import argparse

########################################################
# Anolis Specific definition
########################################################
anbz_str      = 'ANBZ: #16164'

########################################################
# OpenCloudOS specific definition
########################################################
conflict_str  = 'Conflict: none'

########################################################
# OpenEuler specific definition
########################################################
inclusion_str = 'mainline inclusion'
from_str      = 'from mainline-v6.7-rc1'
category_str  = 'category: performance'
bugzilla_str  = 'bugzilla: https://gitee.com/openeuler/intel-kernel/issues/IBP9QO'
cve_str       = 'CVE: NA'

########################################################
# Common definition
########################################################
sig_str       = 'Backport Auto-tune per-CPU pageset size.'
amend_str     = '[ Aubrey Li: amend commit log ]'
sob_str       = 'Signed-off-by: Aubrey Li <aubrey.li@linux.intel.com>'

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
    
def insert_commit_line(patch_text, community):
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
        match community:

            case 'anolis':
                lines.insert(insert_index, f'commit {commit_id} upstream.')
                lines.insert(insert_index, '')
                lines.insert(insert_index, anbz_str)
                lines.insert(insert_index, '')

            case 'baseline':
                lines.insert(insert_index, f'commit {commit_id} upstream.')
                lines.insert(insert_index, '')

            case 'euler':
                lines.insert(insert_index, '--------------------------------')
                lines.insert(insert_index, '')
                lines.insert(insert_index, f'Reference: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id={commit_id}')
                lines.insert(insert_index, '')
                lines.insert(insert_index, cve_str)
                lines.insert(insert_index, bugzilla_str)
                lines.insert(insert_index, category_str)
                lines.insert(insert_index, f'commit {commit_id}')
                lines.insert(insert_index, from_str)
                lines.insert(insert_index, inclusion_str)
                lines.insert(insert_index, '')

            case 'oc':
                lines.insert(insert_index, conflict_str)
                lines.insert(insert_index, f'[ Upstream commit {commit_id} ]')
                lines.insert(insert_index, '')

            case 've':
                lines.insert(insert_index, f'commit {commit_id} upstream.')
                lines.insert(insert_index, '')

            case _:
                raise ValueError("Invalid community name: {community}")
    
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

def process_patch(filename, community):
    with open(filename, "r", encoding="utf-8") as f:
        patch_text = f.read()
    
    patch_text = insert_commit_line(patch_text, community)
    patch_text = insert_intel_sig(patch_text)
    patch_text = insert_signature(patch_text)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(patch_text)

def process_directory(directory, community):
    for filename in os.listdir(directory):
        if filename.endswith(".patch"):  # Ensure we only process .patch files
            file_path = os.path.join(directory, filename)
            process_patch(file_path, community)

def main():

    parser = argparse.ArgumentParser(description="Amend patch script")
    
    parser.add_argument("-c", "--community", required=True,
                        choices=['anolis', 'baseline', 'euler', 'oc', 've'],
                        help="Community name (required)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--patch", help="Specify a patch file")
    group.add_argument("-d", "--directory", help="Specify a directory")
    
    args = parser.parse_args()

    if args.patch:
        process_patch(args.patch, args.community)
    elif args.directory:
        process_directory(args.directory, args.community)

if __name__ == "__main__":
    main()
