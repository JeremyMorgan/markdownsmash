import os
from datetime import datetime

def find_markdown_files(directory: str) -> tuple[list[str], int]:
    """
    This function walks through a given directory and its subdirectories,
    looking for markdown files (with extensions .md or .markdown).
    It returns a list of all found markdown file paths and the total count of files found.

    Parameters:
    directory (str): The root directory to start searching for markdown files.

    Returns:
    tuple[list[str], int]: A tuple containing a list of markdown file paths and the total count of files found.
    """
    markdown_files = []
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                markdown_files.append(os.path.join(root, file))
                file_count += 1
                print(f"Found file {file_count}: {os.path.join(root, file)}")
    return markdown_files, file_count

def read_markdown_content(file_path):
    """
    Reads and processes the content of a markdown file, filtering out specific patterns.
    
    Function is highly focused on markdown for Hugo sites, and JeremyMorgan.com in particular.

    This function opens a markdown file, reads its content line by line, and filters out
    lines that start with certain predefined patterns. The remaining content is joined
    into a single string with spaces between lines.

    Parameters:
    file_path (str): The path to the markdown file to be read and processed.

    Returns:
    str: A string containing the processed content of the markdown file, with filtered
         lines removed and remaining lines joined by spaces.
    """
    content = []
    ignore_patterns = [
        '# slug:', 'tags:', '![', '{{< partial', '[0]:', 
        *[f'[{i}]: /images/' for i in range(38)],
        '---','﻿---',
        'headline: "', 'date:', 'draft:', 'description:', 'section:', '-',
        'lastmod:', 'type:', 'image:', '![',
        '`````'
    ]
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if line and not any(line.startswith(pattern) for pattern in ignore_patterns):
                content.append(line)
    
    # Join all content with spaces instead of newlines
    return ' '.join(content)

def append_to_output_file(content: str, output_file_path: str) -> None:
    """
    Appends the given content to the specified output file.

    This function takes a string of content and appends it to the file specified
    by output_file_path. If the content is not empty, it is written to the file
    with an additional space character. If the content is empty, a message is
    printed indicating that there is no content to append.

    Parameters:
    content (str): The text content to be appended to the file.
    output_file_path (str): The file path where the content should be appended.

    Returns:
    None

    Side effects:
    - Appends content to the specified file if content is not empty.
    - Prints a message indicating the number of characters appended or that no content was appended.
    """
    if content:
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            output_file.write(content + ' ')  # Add a space between file contents
        print(f"Appended {len(content)} characters to {output_file_path}")
    else:
        print("No content to append")

content_directory = './content'
output_file_path = 'combined_markdown_content.txt'

# Clear the output file if it exists
open(output_file_path, 'w').close()

markdown_files, total_files = find_markdown_files(content_directory)

print(f"\nTotal markdown files found: {total_files}")

for file_path in markdown_files:
    print(f"Processing: {file_path}")
    file_content = read_markdown_content(file_path)
    append_to_output_file(file_content, output_file_path)

print(f"\nAll content has been combined into: {output_file_path}")
print(f"Output file size: {os.path.getsize(output_file_path)} bytes")
