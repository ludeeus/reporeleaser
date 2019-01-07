"""Enable CLI."""
import click


@click.command()
@click.option('--token', '-T', default=None, help='GitHub access_token.')
@click.option('--repo', '-R', default=None, help='Repo.')
@click.option('--release', help='Release type.')
@click.option('--test', '-P', is_flag=True, help="Test run.")
@click.option('--version', '-V', is_flag=True, help='Print version.')
def cli(token, repo, release, test, version):
    """CLI for this package."""
    if version:
        from reporeleaser.version import __version__
        print(__version__)
    else:
        from reporeleaser.release import CreateRelease
        create_release = CreateRelease(token, repo, release, test)
        create_release.create_release()


cli()  # pylint: disable=E1120
