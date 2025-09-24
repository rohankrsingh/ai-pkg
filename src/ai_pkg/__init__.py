"""
AIPkg - Your AI-Powered Development Environment Wizard for Arch Linux
Transform plain English into perfectly crafted development environments
"""

try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("ai-pkg")
    except PackageNotFoundError:
        # Package is not installed
        from setuptools_scm import get_version
        try:
            __version__ = get_version(root='..', relative_to=__file__)
        except:
            __version__ = "0.0.0+dev"
except ImportError:
    __version__ = "0.0.0+dev"