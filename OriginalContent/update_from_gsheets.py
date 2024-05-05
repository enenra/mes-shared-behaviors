import os
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom

from datetime import datetime
from bs4 import BeautifulSoup


SPREADSHEETS = {
    'Trigger': ['1YYjm9Y0HpRuZet7RWw_DOT7DHtBBw4czOJ6-K7415cc', 'Rival AI Trigger'],
    'Behavior': ['15nN5NMh0ivqrrG9U6tim4sqW8dcKwvBBvM_peIXn5yc', 'Rival AI Behavior']
}

OUTPUT_DIR = os.path.join(os.getcwd(), 'Content', 'Data', 'MES')


def scrape_spreadsheet(spreadsheet) -> list:
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet[0] + '/gviz/tq?tqx=out:html&tq&gid=1'

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

            if idx in [0, 1]:
                continue

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


def create_mes_parameter(valuename, value=None) -> str:
    if value is None:
        return f"\n\n\t\t\t[{valuename}]\n\n"
    else:
        return f"\t\t\t[{valuename}:{value}]\n"
    

def fix_indents(xml_formatted) -> str:
    xml_formatted = xml_formatted.replace('XMLSchema">', 'XMLSchema">\n')
    xml_formatted = xml_formatted.replace('</EntityComponent>', '</EntityComponent>\n')
    xml_formatted = xml_formatted.replace('</Description>', '\t\t</Description>')
    return xml_formatted


def write_ec_sbc(filetype, rows):

    entries = []
    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            header = row

        else:
            entry = {}
            for idx, item in enumerate(row):
                if item is not None:
                    entry[header[idx]] = item
            entries.append(entry)

    defs = ET.Element('Definitions')
    defs.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    defs.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')

    for e in entries:
        ec = ET.SubElement(defs, 'EntityComponent')
        ec.set('xsi:type', 'MyObjectBuilder_InventoryComponentDefinition')

        id = ET.SubElement(ec, 'Id')
        type_id = ET.SubElement(id, 'TypeId')
        type_id.text = 'Inventory'
        subtype_id = ET.SubElement(id, 'SubtypeId')
        subtype_id.text = e['Name']

        desc = ET.SubElement(ec, 'Description')

        params = create_mes_parameter(SPREADSHEETS[filetype][1])
        for k, v in e.items():
            if k == 'Name':
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

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target_file = os.path.join(OUTPUT_DIR, filetype + '.sbc')
    exported_xml = open(target_file, "w")
    exported_xml.write(xml_formatted)


def main():
    results = {}
    for key, val in SPREADSHEETS.items():
        results = scrape_spreadsheet(val)
        write_ec_sbc(key, results)


if __name__ == '__main__':
    main()