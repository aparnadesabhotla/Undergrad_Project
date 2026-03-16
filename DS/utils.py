import xml.etree.ElementTree as ET

def XMLtoDict(xml):
    """ decodes an xml msg"""
    msg = {}
    parser = ET.XMLPullParser(['start', 'end']) # nãl bloqueante
    parser.feed(xml)
    for event,elem in parser.read_events():
        if(elem.tag!='data'):
            if (str(elem.text).isnumeric()):
                elem.text = int(elem.text)
            msg[elem.tag]=elem.text
    return msg


def dictToXML(dict):
    """ encodes a message in xml

        Parameters:
        dict:msg(dictionary) to encode

    """
    messages = ET.Element('data'); # root

    for key, val in dict.items():
        child = ET.Element(key)
        child.text = str(val)
        messages.append(child)

    return ET.tostring(messages)