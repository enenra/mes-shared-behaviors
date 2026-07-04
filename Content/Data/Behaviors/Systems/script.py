import os
import re

def extract_dialogue_ids(directory):
    dialogue_ids = set()

    # Regex to find [DialogueCueId:SOMETHING]
    pattern = re.compile(r"\[DialogueCueId:(.*?)\]")

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".sbc"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    matches = pattern.findall(content)
                    dialogue_ids.update(matches)
                except UnicodeDecodeError as e:
                    print(f"Error reading {filepath}: {e}")

    # Write sorted results to file
    with open("dialogue_cue_ids.txt", "w", encoding='utf-8') as output_file:
        for dialogue_id in sorted(dialogue_ids):
            output_file.write(dialogue_id + "\n")

    print(f"✅ Extracted {len(dialogue_ids)} DialogueCueIds, saved to dialogue_cue_ids.txt.")

# Run the script on current directory
extract_dialogue_ids('.')
