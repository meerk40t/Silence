from setuptools import setup
setup(
    install_requires=[
        "pyusb>=1.0.0",
        "svgelements",
    ],
    extras_require={
        'all': ['wxPython>=4.0.0', "Pillow>=7.0.0", "ezdxf>=0.13.0"],
        'gui': ['wxPython>=4.0.0', "Pillow>=7.0.0"],
        'dxf': ["ezdxf>=0.13.0"],
    }
)