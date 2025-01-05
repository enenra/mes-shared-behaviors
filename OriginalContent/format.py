import os
import re

def format_sbc(lines):

    print("Before -------------------------------------------------")
    print(lines)

    # XML indents
    result = re.sub(r"\s*(?=<\?xml)", "", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Definitions)", "", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<EntityComponents>)", "  ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</EntityComponents>)", "  ", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<EntityComponent )", "    ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</EntityComponent>)", "    ", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Id>)", "      ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</Id>)", "      ", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<TypeId>)", "      ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</TypeId>)", "      ", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<SubtypeId>)", "      ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</SubtypeId>)", "      ", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Description>)", "      ", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</Description>)", "      ", lines, flags=re.MULTILINE)

    # XML formatting
    #result = re.sub(r"</Description>\s*\n\s*</EntityComponent>", "</Description>\n    </EntityComponent>", lines, flags=re.MULTILINE)

    # MES Tag formatting
    result = re.sub(r"^\s*\[", "        [", result, flags=re.MULTILINE)

    print("After -------------------------------------------------")
    print(result)

    return result


def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.sbc') and filename.startswith("System_Disabled"):
                with open(os.path.join(root, filename), 'r+') as f:
                    result = format_sbc(f.read())
                    f.seek(0)
                    f.write(result)
                    f.truncate()
                    return


def main():
    data = os.path.join(os.getcwd(), 'Content', 'Data')
    behaviors = os.path.join(data, 'Behaviors')
    target_profiles = os.path.join(data, 'TargetProfiles')

    iterate_files(behaviors)
    iterate_files(target_profiles)

if __name__ == '__main__':
    main()