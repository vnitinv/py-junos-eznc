
"""
Advance feature toolkit
"""

from jnpr.junos import Device


class AFI(object):
    """
    The SCP utility is used to conjunction with :class:`jnpr.junos.utils.sw.SW`
    when transferring the Junos image to the device.  The :class:`SCP` can be
    used for other secure-copy use-cases as well; it is implemented to support
    the python *context-manager* pattern.  For example::

        from jnpr.junos.utils.scp import SCP

        with SCP(dev, progress=True) as scp:
            scp.put(package, remote_path)

    """

    def __init__(self, junos, target):
        """
        Constructor that wraps :py:mod:`paramiko` and :py:mod:`scp` objects.

        :param Device junos: the Device object
        :param str target : FPC to be connected
        """
        self.target = target

        self.chan = Device(host=junos._hostname,
                           port=junos._port,
                           user=junos._auth_user,
                           password=junos._auth_password,
                           key_filename=junos._ssh_private_key_file,
                           ssh_config=junos._sshconf_lkup())

    def open(self, **kwargs):
        """
        Creates an instance of the ncclient manager similar to Device class
        """
        self.chan._device_params['target'] = self.target
        self.chan.open()

    def close(self):
        """
        Closes the ssh/scp connection to the device
        """
        self.chan.close()

    # -------------------------------------------------------------------------
    # CONTEXT MANAGER
    # -------------------------------------------------------------------------

    def __enter__(self):
        self.open()
        return self.chan

    def __exit__(self, exc_ty, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return "Device(%s:%s)" % (self.hostname, self.target)
