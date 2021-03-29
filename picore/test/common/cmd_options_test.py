import unittest
import picore.common.CmdOptions as options


class MyTestCase(unittest.TestCase):
    def test_read_static(self):
        opts = options.CmdOptions()
        opts.add_option('test1', '-t1', ['--test1'], required=True)
        opts.add_option('testi', '-i', ['--int'])
        opts.add_option('testf', '-f', ['--float'])

        opts.read_static(['-t1 string', '--int 2365', '-f 56.999'])
        for key in opts.options:
            opt = opts.options[key]
            print('[option=' + opt.name + ', value=' + opt.value)


if __name__ == '__main__':
    unittest.main()
