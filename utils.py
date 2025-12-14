import xml.etree.ElementTree as ET
from flask import jsonify
from datetime import datetime

def format_response(data, format_type):
    if format_type == 'xml':
        root = ET.Element("players")
        
        # Convert tuple to list if needed
        if isinstance(data, tuple):
            data = list(data)
        elif not isinstance(data, list):
            data = [data] if data else []
        
        for row in data:
            if isinstance(row, dict):
                player = ET.SubElement(root, "player")
                for key, value in row.items():
                    # Convert datetime objects to strings
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    ET.SubElement(player, key).text = str(value)
        
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding='unicode')
        return xml_str, 200, {'Content-Type': 'application/xml'}
    return jsonify(data)

def parse_xml_request(xml_data):
    """Parse XML request body and return dictionary"""
    try:
        root = ET.fromstring(xml_data)
        data = {}
        for child in root:
            data[child.tag] = child.text
        return data
    except Exception as e:
        return None

def xml_response(message, status_code=200, data_dict=None):
    """Create an XML response for messages or single object"""
    root = ET.Element("response")
    ET.SubElement(root, "message").text = message
    if data_dict:
        for key, value in data_dict.items():
            if isinstance(value, datetime):
                value = value.isoformat()
            ET.SubElement(root, key).text = str(value)
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding='unicode')
    return xml_str, status_code, {'Content-Type': 'application/xml'}
