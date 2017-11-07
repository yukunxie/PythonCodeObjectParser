import sys
reload(sys)
sys.setdefaultencoding('utf8')

import dis 
import types
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

code = '''
a = 10
b = 20
c = a + b
def f(a):
	def tes():
		pass
	z = 30
	return z
'''

co = compile(code, "co.py", "exec")


def getCodeObjectName(co):
	"<code object f at 023E14A0,"
	text = str(co)
	idx = text.find("at")
	text = text[0:idx].replace("<code object", "").replace(" ", "")
	return text

def __parseCodeObjectNode(xmlNode, co):
	constsNode = ET.SubElement(xmlNode, "co_consts")
	for idx, const in enumerate(co.co_consts):
		if type(const) == types.CodeType:
			node_name = ET.SubElement(constsNode, "item")
			node_name.attrib["name"] = getCodeObjectName(const)
			node_name.attrib["type"] = "codeobject"
			__parseCodeObjectNode(node_name, const)
		else:
			node_name = ET.SubElement(constsNode, "item")
			node_name.text = str(const)
		node_name.attrib['idx'] = str(idx)
	constsNode.attrib["count"] = str(len(co.co_consts))

	
	nameNode = ET.SubElement(xmlNode, "co_names")
	for idx, name in enumerate(co.co_names):
		node_name = ET.SubElement(nameNode, "name")
		node_name.text = str(name)
		node_name.attrib['idx'] = str(idx)
	nameNode.attrib["count"] = str(len(co.co_names))


	nameNode = ET.SubElement(xmlNode, "co_varnames")
	for idx, name in enumerate(co.co_varnames):
		node_name = ET.SubElement(nameNode, "name")
		node_name.text = str(name)
		node_name.attrib['idx'] = str(idx)
	nameNode.attrib["count"] = str(len(co.co_varnames))

	
	nameNode = ET.SubElement(xmlNode, "co_filename")
	nameNode.text = co.co_filename

	nameNode = ET.SubElement(xmlNode, "co_ename")
	nameNode.text = co.co_name

	nameNode = ET.SubElement(xmlNode, "co_nlocals")
	nameNode.text = str(co.co_nlocals)

	nameNode = ET.SubElement(xmlNode, "co_stacksize")
	nameNode.text = str(co.co_stacksize)

	nameNode = ET.SubElement(xmlNode, "co_argcount")
	nameNode.text = str(co.co_argcount)


def parseCodeObjectNodeWithCo(co, xmlFilename):
	root_name = ET.Element("codeobject")
	__parseCodeObjectNode(root_name, co)
	
	rough_string = ET.tostring(root_name, 'utf-8')
	reared_content = minidom.parseString(rough_string)
	with open(xmlFilename, 'w') as fs:
		reared_content.writexml(fs, addindent=" ", newl="\n", encoding="utf-8")


def parseCodeObjectNodeWithCodeSnippet(codestring, xmlFilename):
	co = compile(codestring, xmlFilename.replace(".xml", ".py"), "exec")
	parseCodeObjectNodeWithCo(co, xmlFilename)


def parseCodeObjectNodeWithPyFile(pyFilename, xmlFilename):
	with open(pyFilename) as fd:
		text = fd.read()
		parseCodeObjectNodeWithCodeSnippet(text, xmlFilename)


if __file__ == "__main__":
	parseCodeObjectNodeWithPyFile(r"codeobject.py", "camera.xml")
