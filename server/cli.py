import click


@click.group()
def cli():
    """Base command group."""
    pass


@cli.command('fetch')
def fetch():
    """
    Fetches data from officequotes.net, placing them in unmodified UTF-8 HTML files.
    """
    pass


@cli.command('process')
def process():
    """
    Processes manually processed raw quote data into JSON.
    """
    pass


@cli.group('build')
def build():
    """Data building command group."""
    pass


@build.command('algolia')
def algolia():
    """
    Generates algolia.json, a all encompassing file for Algolia's search index.
    """
    pass


@build.command('final')
def final():
    """Generates the latest application static data.json file, used by the backend API."""
    pass


if __name__ == "__main__":
    cli()
