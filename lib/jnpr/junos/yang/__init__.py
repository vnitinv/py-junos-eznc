from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.config import Config


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