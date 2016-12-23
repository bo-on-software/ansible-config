#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

class GConftool2(object):
    """Wrapper class to interact with gconftool-2"""
    def __init__(self, module):
        self.module = module
        self.command = module.get_bin_path('gconftool-2')
        if self.command is None:
            raise RuntimeError("Can't find gconftool-2 binary")

    def set(self, key, value_type, value):
        rc, out, err = self._exec('--type ' + value_type + ' --set ' + key + ' ' + value)

    def get(self, key):
        rc, out, err = self._exec('--get-type --get ' + key)
        results = out.split('\n')
        value      = results[0] if len(results) > 0 else None
        value_type = results[1] if len(results) > 1 else None
        return value_type, value

    def _exec(self, command):
        return self.module.run_command(self.command + ' ' + command, check_rc = True)

def main():
    module = AnsibleModule(
        argument_spec = {
            'key':   {'required': True, 'type': 'str'},
            'type':  {'required': True, 'type': 'str'},
            'value': {'required': True, 'type': 'str'}
        }
    )

    try:
        gconf = GConftool2(module)
        key = module.params.get('key')
        value_type = module.params.get('type')
        value = module.params.get('value')

        old_value_type, old_value = gconf.get(key)
        if value_type == old_value_type and value == old_value:
            module.exit_json(changed=False)
        else:
            gconf.set(key, value_type, value)
            module.exit_json(changed=True, old_value=old_value, new_value=value)
    except Exception, ex:
        module.fail_json(msg='Failed: ' + str(ex))

if __name__ == '__main__':
    main()
