#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

class DConf(object):
    """Wrapper class to interact with dconf"""
    def __init__(self, module):
        self.module = module
        self.command = module.get_bin_path('dconf')
        if self.command is None:
            raise RuntimeError("Can't find dconf binary")

    def set(self, key, value):
        rc, out, err = self._exec('write ' + key + ' ' + value)

    def get(self, key):
        rc, out, err = self._exec('read ' + key)
        return out.strip('\n')

    def _exec(self, command):
        return self.module.run_command(self.command + ' ' + command, check_rc = True)

def main():
    module = AnsibleModule(
        argument_spec = {
            'key': {'required': True, 'type': 'str'},
            'value': {'required': True, 'type': 'str'}
        }
    )

    try:
        dconf = DConf(module)
        key = module.params.get('key')
        value = module.params.get('value')

        old_value = dconf.get(key)
        if value == old_value:
            module.exit_json(changed=False)
        else:
            dconf.set(key, value)
            module.exit_json(changed=True, old_value=old_value, new_value=value)
    except Exception, ex:
        module.fail_json(msg='Failed: ' + str(ex))

if __name__ == '__main__':
    main()
