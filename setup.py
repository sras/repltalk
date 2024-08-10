from setuptools import setup, find_packages

setup(
    name = "pyrepltalk",
    description='Talk to REPLs from code editors',
    url='http://github.com/sras/repltalk',
    author='Sandeep.C.R',
    author_email='sandeep@sras.me',
    license='MIT',
    version = "1.1.1",
    packages = ['repltalk', 'repltalk.servers', 'repltalk.adapters'],
    entry_points = {
        "console_scripts":['elm18_server=repltalk.servers.elm18:main',
            'elm_server=repltalk.servers.elm:main',
            'typescript_watcher=repltalk.servers.typescript:main',
            'haskell_watcher=repltalk.servers.haskell_build:main',
            'rust_watcher=repltalk.servers.rust_build:main',
            'fun_c_watcher=repltalk.servers.fun_c_build:main',
            'solidity_watcher=repltalk.servers.solidity:main',
            'haskell_server=repltalk.servers.haskell:main',
            'nvim_adapter=repltalk.adapters.nvim:main',
            'vim_adapter=repltalk.adapters.vim:main']
    },
    install_requires=[ 'pexpect', 'bottle' ]
)
