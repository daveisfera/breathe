
from unittest import TestCase
from xml.dom import minidom

from breathe.renderer.rst.doxygen.compound import get_param_decl
from breathe.parser.doxygen.compoundsuper import memberdefType

class TestUtils(TestCase):

    def test_param_decl(self):

        # From xml from: examples/specific/parameters.h
        xml = """
        <memberdef>
        <param>
          <type>int</type>
          <declname>a</declname>
        </param>
        <param>
          <type>float</type>
          <declname>b</declname>
        </param>
        <param>
          <type>int *</type>
          <declname>c</declname>
        </param>
        <param>
          <type>int(*)</type>
          <declname>p</declname>
          <array>[3]</array>
        </param>
        <param>
          <type><ref refid="class_my_class" kindref="compound">MyClass</ref></type>
          <declname>a</declname>
        </param>
        <param>
          <type><ref refid="class_my_class" kindref="compound">MyClass</ref> *</type>
          <declname>b</declname>
        </param>
        </memberdef>
        """

        doc = minidom.parseString(xml)

        memberdef = memberdefType.factory()
        for child in doc.documentElement.childNodes:
            memberdef.buildChildren(child, 'param')

        self.assertEqual(get_param_decl(memberdef.param[0]), 'int a')
        self.assertEqual(get_param_decl(memberdef.param[1]), 'float b')
        self.assertEqual(get_param_decl(memberdef.param[2]), 'int * c')
        self.assertEqual(get_param_decl(memberdef.param[3]), 'int(*p)[3]')
        self.assertEqual(get_param_decl(memberdef.param[4]), 'MyClass a')
        self.assertEqual(get_param_decl(memberdef.param[5]), 'MyClass  * b')
