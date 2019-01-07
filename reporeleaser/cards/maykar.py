"""Generate json form maykar."""
from reporeleaser.defaults import REUSE, VISIT


def get_data(github, selected_repos):
    """Generate json form maykar."""
    org = 'maykar'
    data = {}
    repos = []
    all_repos = ['compact-custom-header']
    if selected_repos:
        for repo in selected_repos:
            if repo in all_repos:
                repos.append(repo)
    else:
        repos = all_repos
    for repo in repos:
        try:
            repo = github.get_repo(org + '/' + repo)
            name = repo.name
            print("Generating json for repo:", name)

            release = list(repo.get_releases())[0]

            updated_at = repo.updated_at.isoformat().split('T')[0]

            version = release.tag_name

            remote_location = REUSE.format(org, name, name)
            remote_location = remote_location + '.js'

            visit_repo = VISIT.format(org, name)

            changelog = release.html_url

            data[name] = {}
            data[name]['updated_at'] = updated_at
            data[name]['version'] = version
            data[name]['remote_location'] = remote_location
            data[name]['visit_repo'] = visit_repo
            data[name]['changelog'] = changelog
        except Exception:  # pylint: disable=W0703
            pass
    return data
