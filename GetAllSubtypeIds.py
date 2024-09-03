import os
import re

def extract_subtypeids(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove all content inside comments
    content_without_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Find all occurrences of <SubtypeId>...</SubtypeId> outside comments
    subtypeids = re.findall(r'<SubtypeId>(.*?)</SubtypeId>', content_without_comments)

    return subtypeids

def process_folder(folder_path):
    all_subtypeids = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.sbc'):
                file_path = os.path.join(root, file)
                subtypeids = extract_subtypeids(file_path)
                all_subtypeids.extend(subtypeids)

    return all_subtypeids

# Get the folder path where this script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Extract all SubtypeIds
subtypeids = process_folder(folder_path)

# Print the collected SubtypeIds
for subtypeid in subtypeids:
    print(subtypeid)

# Optional: Save the collected SubtypeIds to a file
with open('subtypeids.txt', 'w', encoding='utf-8') as file:
    for subtypeid in subtypeids:
        file.write(subtypeid + '\n')

# Wait for the user to press any key before closing
input("Druk op een toets om te sluiten...")
