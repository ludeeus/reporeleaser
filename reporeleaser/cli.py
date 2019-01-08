"""Enable CLI."""
import click


@click.command()
@click.option('--token', default=None, help='GitHub access_token.')
@click.option('--repo', default=None, help='Repo.')
@click.option('--release', help='Release type.')
@click.option('--test', is_flag=True, help="Test run.")
@click.option('--title', help='Title of the release.')
@click.option('--draft', is_flag=True, help="Creates release draft.")
@click.option('--prerelease', is_flag=True, help="Creates pre release.")
@click.option('--show_sha', is_flag=True,
              help="Show sha in description lines.")
@click.option('--hide_footer', is_flag=True,
              help="Hide footer from description.")
@click.option('--hide_full_changelog', is_flag=True,
              help="Hide Full changelog link from description.")
@click.option('--version', '-V', is_flag=True, help='Print version.')
def cli(token, repo, release, test, title, draft, prerelease, show_sha,
        hide_footer, hide_full_changelog, version):
    """CLI for this package."""
    if version:
        from reporeleaser.version import __version__
        print(__version__)
    else:
        from reporeleaser.release import CreateRelease
        create_release = CreateRelease(token, repo, release, test, title,
                                       draft, prerelease, show_sha,
                                       hide_footer, hide_full_changelog)
        create_release.create_release()


cli()  # pylint: disable=E1120
