from setuptools import setup, find_packages

setup(
    name='Obsidian-Anki-Formatter',
    version='0.1.0',
    author='niposch',
    author_email='niposch@gmail.com',
    description='A GUI for converting obsidian flavored markdown to anki',
    url='https://github.com/niposch/obsidian-anki-formatter',
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            # If your __main__.py file is inside a package called 'src', this should be 'obsidian-anki-formatter=src.__main__:main',
            # You need to define a main() function in your __main__.py file
            'obsidian-anki-formatter=__main__:main',
        ],
    },
    python_requires='>=3.6',  # Minimum version of Python that your project supports
)
