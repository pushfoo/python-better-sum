# Contributing

## Reporting Bugs & Proposing Changes 

Use the GitHub Issues page:

1. Go to [https://github.com/pushfoo/python-better-sum/issues]()
2. Search for existing closed and open issues
3. If none seem relevant, file a new one!

## Contributor Setup

Before you contribute code, you'll need to get your development
environment set up.

[Fork and locally clone]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
[venv]: https://docs.python.org/3/library/venv.html
[This comment]: https://github.com/mkdocstrings/mkdocstrings/issues/215#issuecomment-759591821
[mkdocstrings issue #215]: https://github.com/mkdocstrings/mkdocstrings/issues/215

After making sure you have Python 3.9+:

1. [Fork and locally clone] the repo
2. Create and activate a virtual environment
    * [venv][] is the default
    * others probably work too
3. `pip install --upgrade pip`
4. `pip install -I -e .[dev]`
6. For users Python's standard [venv][] tool:
    1. `deactivate` the virtual environment
    2. reactivate it as described in the [venv][] doc

Per the comments on  reactivation seems to be necessary on the default [venv][]. Poetry
and Rye  are unaffected. To learn more, please see:

* [This comment][] on [mkdocstrings issue #215][]
* The other comments in the same thread 

## Making Changes

### Code Changes

[the project's pyproject.toml]: https://github.com/pushfoo/Fontknife/blob/main/pyproject.toml

The project aims to be simple.

* Remove items from [the project's pyproject.toml][] dependencies section
* Don't add them without a very compelling reason

!!! important

    This is different than the [project.optional-dependencies] section!

### Documentation

[original Markdown]: https://daringfireball.net/projects/markdown/
[Python-Markdown]: https://python-markdown.github.io/
[mkdocs/issues/1385]: https://github.com/mkdocs/mkdocs/issues/1385
[Github-flavored Markdown]: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/about-writing-and-formatting-on-github
[mkdocstrings]: https://mkdocstrings.github.io/

Documentation dependencies can be added if needed to make the
doc better.

At the moment, this project uses:

* [Mkdocs][]
* [mkdocstrings][]

This means we aren't using the [original Markdown] from 2004. Instead, we
the following dialects:

| Markdown Flavor              | Where it's used                                            |
|------------------------------|------------------------------------------------------------|
| [Python-Markdown][]          | Docstrings and everything in the repo's `docs` folder      |
| [GitHub-flavored Markdown][] | Only top-level files in the GitHub repo ([README.md], etc) |



