import json

from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.config import Config
from lxml import etree
from lxml.builder import E
from pyangbind.lib.serialise import pybindIETFJSONEncoder
import jxmlease

class YANG(SW, Config):
    def __init__(self, dev):
        super(YANG, self).__init__(dev)
        self._dev = dev

    def delete(self, package, progress=False, timeout=300, **kwargs):
        """
        This function can be used to delete installed yang package
        Underhood rpc called: request-package-delete
        :return: True/False
        """
        def _progress(report):
            if progress is True:
                self.progress(self._dev, report)
            elif callable(progress):
                progress(self._dev, report)

        rsp = self.rpc.request_package_delete(package_name=package,
                                              dev_timeout=timeout, **kwargs)
        got = rsp.getparent()
        rc = int(got.findtext('package-result').strip())
        output_msg = '\n'.join([i.text for i in got.findall('output')
                                if i.text is not None])
        _progress("request system software delete %s:\nOutput: %s" % (package,
            output_msg))
        return rc == 0

    def load(self, conf):
        conf = json.loads(json.dumps(
            pybindIETFJSONEncoder.generate_element(conf, flt=True),
            cls=pybindIETFJSONEncoder, indent=4))
        conf_xml = jxmlease.emit_xml(conf, full_document=False).encode('utf-8')
        parser = etree.XMLParser(recover=True)
        conf_xml = etree.fromstring(conf_xml, parser)
        conf_xml.set('xmlns', "http://openconfig.net/yang/bgp")
        conf_xml = E('edit-config', E('config', conf_xml))
        print etree.tostring(conf_xml)
        return self._dev.execute(conf_xml)