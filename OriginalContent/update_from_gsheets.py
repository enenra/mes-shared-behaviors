import os
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom

from datetime import datetime
from bs4 import BeautifulSoup


SPREADSHEETS = {
    'Autopilot': ['1wb4ar82IzcofB7UOXgYEwL2NCnCJINZJwdNL8tqZFqw', ['0'], 'Rival AI Autopilot', 'Encounters'],
    'Behavior': ['15nN5NMh0ivqrrG9U6tim4sqW8dcKwvBBvM_peIXn5yc', ['0'], 'Rival AI Behavior', 'Encounters'],
    'Chat': ['1D_DgYZQPQT22zH-mBNHSuX4cLQti6FmzTol7dZxKuPM', ['0'], 'Rival AI Chat', 'Encounters'],
    'Command': ['1EZFc7ibb-ydU1wsSGNfuIIJk_dc2pL7khkFqS-UUFPc', ['0'], 'Rival AI Command', 'Encounters'],
    'Trigger': ['1YYjm9Y0HpRuZet7RWw_DOT7DHtBBw4czOJ6-K7415cc', ['0'], 'Rival AI Trigger', 'Encounters'],
    'TriggerGroup': ['1Yw4pItiEtsliY997-DWA7nZp0XmI483Rhh174jDYpiw', ['0'], 'Rival AI TriggerGroup', 'Encounters']
}

OUTPUT_DIR = os.path.join(os.getcwd(), 'Content', 'Data')


def scrape_spreadsheet(spreadsheet, grid) -> list:
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet[0] + '/gviz/tq?tqx=out:html&tq&gid=' + grid

    html = requests.get(spreadsheet_url).text
    soup = BeautifulSoup(html, 'lxml')

    salas_cine = soup.find_all('table')[0]
    rows = [[td.text for td in row.find_all("td")] for row in salas_cine.find_all('tr')]

    formatted_list = []
    for row in rows:
        if row[0] in ['', '\xa0']:
            continue

        row_list = []
        header_list = []
        for idx, cell in enumerate(row):
            if row[0] == '*Internal* Reference':
                cell = cell.replace(" ", "")

            if cell[0] == '*':
                end = cell[1:].find('*')
                extracted = cell[1:end+1]

                offset = len(header_list) + 2 - idx
                #print(f"{cell} | {len(header_list)} + 2 - {idx} = {offset}")

                for i in range(0,offset):
                    header_list.append(None)

                header_list.append(extracted)


            if cell == '\xa0' or cell == '':
                row_list.append(None)

            elif cell == '✔':
                row_list.append(True)

            elif cell == '✗':
                row_list.append(False)

            elif cell[0] == '*':
                end = cell[1:].find('*')
                if cell[end+3:] == '':
                    row_list.append(cell[1:end+1])
                else:
                    row_list.append(cell[end+2:])

            else:
                row_list.append(cell)
        
        #if len(header_list) > 0:
        #    formatted_list.append(header_list)

        formatted_list.append(row_list)
        
    return formatted_list


def insert_into_entry(entries, header, name, value):
    for et in entries.values():
        for e in et:
            if e['Name'] == name:
                if isinstance(e[header], list):
                    e[header].append(value)
                else:
                    temp = e[header]
                    e[header] = []
                    e[header].append(temp)
                    e[header].append(value)            


def reorganize_table_to_dict(rows) -> dict:

    entries = {}
    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            header = row

        else:
            if row[1] != "1":
                for idx, item in enumerate(row):
                    if item not in [False, None] and idx not in [0, 1]:
                        insert_into_entry(entries, header[idx], row[0], item)

            else:
                entry = {}
                for idx, item in enumerate(row):
                    if idx == 2:
                        if item is None:
                            encounter_type = "Invalid"
                        else:
                            encounter_type = item
                        continue

                    if item is not None:
                        entry[header[idx]] = item

                if encounter_type in entries:
                    entries[encounter_type].append(entry)
                else:
                    entries[encounter_type] = [entry]

    return entries


def create_mes_parameter(valuename, value=None) -> str:
    if value is None:
        return f"\n\n\t\t\t[{valuename}]\n\n"
    elif isinstance(value, list):
        params = ""
        for i in value:
            params += f"\t\t\t[{valuename}:{i}]\n"
        return params
    else:
        return f"\t\t\t[{valuename}:{value}]\n"
    

def fix_indents(xml_formatted) -> str:
    xml_formatted = xml_formatted.replace('XMLSchema">', 'XMLSchema">\n')
    xml_formatted = xml_formatted.replace('</EntityComponent>', '</EntityComponent>\n')
    xml_formatted = xml_formatted.replace('</Description>', '\t\t</Description>')
    return xml_formatted


def write_ec_sbc(filetype, rows):

    entries = reorganize_table_to_dict(rows)

    for et, et_content in entries.items():
        defs = ET.Element('Definitions')
        defs.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        defs.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')

        for e in et_content:
            ec = ET.SubElement(defs, 'EntityComponent')
            ec.set('xsi:type', 'MyObjectBuilder_InventoryComponentDefinition')

            id = ET.SubElement(ec, 'Id')
            type_id = ET.SubElement(id, 'TypeId')
            type_id.text = 'Inventory'
            subtype_id = ET.SubElement(id, 'SubtypeId')
            subtype_id.text = e['Name']

            desc = ET.SubElement(ec, 'Description')

            params = create_mes_parameter(SPREADSHEETS[filetype][2])
            for k, v in e.items():
                if k in ['Reference', '#','Name']:
                    continue
                params += create_mes_parameter(k, v)
            
            params += '\n'
            desc.text = params

        temp_string = ET.tostring(defs, 'utf-8')
        temp_string.decode('ascii')
        xml_string = xml.dom.minidom.parseString(temp_string)
        xml_formatted = xml_string.toprettyxml()

        xml_formatted = fix_indents(xml_formatted)
        xml_formatted = xml_formatted.replace('<?xml version="1.0" ?>', f'<?xml version="1.0"?>\n\n<!-- Created from GSheet export on {datetime.now()} -->\n')

        path = os.path.join(OUTPUT_DIR, SPREADSHEETS[filetype][3], et)
        os.makedirs(path, exist_ok=True)
        target_file = os.path.join(path, 'MSB_' + filetype + '_' + et + '.sbc')
        exported_xml = open(target_file, "w")
        exported_xml.write(xml_formatted)


def main():

    SPREADSHEETS = {'Condition': ['1bdBapnrTcWX9HCxr75W0_db3sMRuE0Ws_9QyA23ew9A', ['0', '1403879885', '253248836', '504907006'], 'Rival AI Condition', 'Encounters']}

    results = {}
    for key, val in SPREADSHEETS.items():
        results = []
        for grid in val[1]:
            results.append(scrape_spreadsheet(val, grid))
        write_ec_sbc(key, results)


if __name__ == '__main__':
    main()