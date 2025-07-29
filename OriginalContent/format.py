import os
import re

def format_sbc(lines):

    # XML indents
    result = re.sub(r"\s*(?=<\?xml)", "", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Definitions)", "", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<EntityComponents>)", "\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</EntityComponents>)", "\t", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<EntityComponent )", "\t\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</EntityComponent>)", "\t\t", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Id>)", "\t\t\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</Id>)", "\t\t\t", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<TypeId>)", "\t\t\t\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</TypeId>)", "\t\t\t\t", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<SubtypeId>)", "\t\t\t\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</SubtypeId>)", "\t\t\t\t", lines, flags=re.MULTILINE)

    result = re.sub(r"\s*(?=<Description>)", "\t\t\t", lines, flags=re.MULTILINE)
    result = re.sub(r"\s*(?=</Description>)", "\t\t\t", lines, flags=re.MULTILINE)

    # MES Tag formatting
    result = re.sub(r"^\s*(?=\[)", "\t\t\t\t[", result)

    return result


def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.sbc'):
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