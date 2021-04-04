import unittest
import pir2.common.CmdOptions as options


class MyTestCase(unittest.TestCase):
    def test_read_static(self):
        opts = options.CmdOptions()
        opts.add_option('test1', '-t1', ['--test1'], required=True, description='Required String parameter')
        opts.add_option('testi', '-i', ['--int'], required=True, description='Required int parameter')
        opts.add_option('testf', '-f', ['--float'], description='Optional float parameter')

        opts.read_static(['--test1', 'string', '--int', '2365', '-f', '56.999'])
        for key in opts.options:
            opt = opts.options[key]
            print('[option=' + opt.name + ', value=' + str(opt.value))


if __name__ == '__main__':
    unittest.main()
