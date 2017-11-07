import sys
reload(sys)
sys.setdefaultencoding('utf8')

import dis 
import types
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def getCodeObjectName(co):
	"<code object f at 023E14A0,"
	text = str(co)
	idx = text.find("at")
	text = text[0:idx].replace("<code object", "").replace(" ", "")
	return text

def __parseCodeObjectNode(xmlNode, co):
	subNode = ET.SubElement(xmlNode, "co_consts")
	for idx, const in enumerate(co.co_consts):
		if type(const) == types.CodeType:
			itemNode = ET.SubElement(subNode, "item")
			itemNode.attrib["name"] = getCodeObjectName(const)
			itemNode.attrib["type"] = "codeobject"
			__parseCodeObjectNode(itemNode, const)
		else:
			itemNode = ET.SubElement(subNode, "item")
			itemNode.text = str(const)
		itemNode.attrib['idx'] = str(idx)
	subNode.attrib["count"] = str(len(co.co_consts))
	
	subNode = ET.SubElement(xmlNode, "co_names")
	for idx, name in enumerate(co.co_names):
		itemNode = ET.SubElement(subNode, "name")
		itemNode.text = str(name)
		itemNode.attrib['idx'] = str(idx)
	subNode.attrib["count"] = str(len(co.co_names))

	subNode = ET.SubElement(xmlNode, "co_varnames")
	for idx, name in enumerate(co.co_varnames):
		itemNode = ET.SubElement(subNode, "name")
		itemNode.text = str(name)
		itemNode.attrib['idx'] = str(idx)
	subNode.attrib["count"] = str(len(co.co_varnames))

	subNode = ET.SubElement(xmlNode, "co_filename")
	subNode.text = co.co_filename

	subNode = ET.SubElement(xmlNode, "co_ename")
	subNode.text = co.co_name

	subNode = ET.SubElement(xmlNode, "co_nlocals")
	subNode.text = str(co.co_nlocals)

	subNode = ET.SubElement(xmlNode, "co_stacksize")
	subNode.text = str(co.co_stacksize)

	subNode = ET.SubElement(xmlNode, "co_argcount")
	subNode.text = str(co.co_argcount)


def parseCodeObjectNodeWithCo(co, xmlFilename):
	rootNode = ET.Element("codeobject")
	__parseCodeObjectNode(rootNode, co)
	
	rough_string = ET.tostring(rootNode, 'utf-8')
	reared_content = minidom.parseString(rough_string)
	with open(xmlFilename, 'w') as fs:
		reared_content.writexml(fs, addindent="    ", newl="\n", encoding="utf-8")


def parseCodeObjectNodeWithCodeSnippet(codestring, xmlFilename):
	co = compile(codestring, xmlFilename.replace(".xml", ".py"), "exec")
	parseCodeObjectNodeWithCo(co, xmlFilename)


def parseCodeObjectNodeWithPyFile(pyFilename, xmlFilename):
	with open(pyFilename) as fd:
		text = fd.read()
		parseCodeObjectNodeWithCodeSnippet(text, xmlFilename)


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

if __name__ == "__main__":
	parseCodeObjectNodeWithPyFile(r"codeparser.py", "codeparser.xml")
