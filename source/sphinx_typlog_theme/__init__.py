import os
__version__ = '0.6.2'


def get_path():
    """Shortcut for users to access this theme. If you are using
    Sphinx < 1.7, you can add it into html_theme_path::

        import sphinx_typlog_theme
        html_theme_path = [sphinx_typlog_theme.get_path()]

    :return: theme path
    """
    # Theme directory is defined as our parent directory
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def add_badge_roles(app):
    from docutils.nodes import inline, make_id
    from docutils.parsers.rst.roles import set_classes

    def create_badge_role(color=None):
        def badge_role(name, rawtext, text, lineno, inliner,
                       options=None, content=None):
            options = options or {}
            set_classes(options)
            classes = ['badge']
            if color is None:
                classes.append('badge-' + make_id(text))
            else:
                classes.append('badge-' + color)
            if len(text) == 1:
                classes.append('badge-one')
            options['classes'] = classes
            node = inline(rawtext, text, **options)
            return [node], []
        return badge_role

    app.add_role('badge', create_badge_role())
    app.add_role('badge-red', create_badge_role('red'))
    app.add_role('badge-blue', create_badge_role('blue'))
    app.add_role('badge-green', create_badge_role('green'))
    app.add_role('badge-yellow', create_badge_role('yellow'))


def add_github_roles(app, repo):
    """Add ``gh`` role to your sphinx documents. It can generate GitHub
    links easily::

        :gh:`issue#57` will generate the issue link
        :gh:`PR#85` will generate the pull request link

    Use this function in ``conf.py`` to enable this feature::

        def setup(app):
            sphinx_typlog_theme.add_github_roles(app, 'lepture/authlib')

    :param app: sphinx app
    :param repo: GitHub repo, e.g. "lepture/authlib"
    """
    from docutils.nodes import reference
    from docutils.parsers.rst.roles import set_classes

    base_url = 'https://github.com/{}'.format(repo)

    def github_role(name, rawtext, text, lineno, inliner,
                    options=None, content=None):
        if '#' in text:
            t, n = text.split('#', 1)
            if t.lower() in ['issue', 'issues']:
                url = base_url + '/issues/{}'.format(n)
            elif t.lower() in ['pr', 'pull', 'pull request']:
                url = base_url + '/pull/{}'.format(n)
            elif t.lower() in ['commit', 'commits']:
                url = base_url + '/commit/{}'.format(n)
        else:
            url = base_url + '/' + text

        options = options or {'classes': ['gh']}
        set_classes(options)
        node = reference(rawtext, text, refuri=url, **options)
        return [node], []

    app.add_role('gh', github_role)


def setup(app):
    # add_html_theme is new in Sphinx 1.6+
    if hasattr(app, 'add_html_theme'):
        theme_path = os.path.abspath(os.path.dirname(__file__))
        app.add_html_theme('sphinx_typlog_theme', theme_path)

    return {'version': __version__, 'parallel_read_safe': True}
