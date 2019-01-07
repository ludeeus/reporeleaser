"""Generate json form thomasloven."""
from reporeleaser.defaults import REUSE, VISIT


def get_data(github, selected_repos):
    """Generate json form thomasloven."""
    org = 'thomasloven'
    data = {}
    repos = []
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        try:
            repo = github.get_repo(org + '/' + repo)
            if 'lovelace-' in repo.name:
                name = repo.name.replace('lovelace-', '')
                fullname = repo.name
                print("Generating json for repo:", name)

                updated_at = repo.updated_at.isoformat().split('T')[0]

                version = list(repo.get_commits())[0].sha[0:6]

                remote_location = REUSE.format(org, fullname, name)
                remote_location = remote_location + '.js'

                visit_repo = VISIT.format(org, fullname)

                changelog = VISIT.format(org, fullname)

                data[name] = {}
                data[name]['updated_at'] = updated_at
                data[name]['version'] = version
                data[name]['remote_location'] = remote_location
                data[name]['visit_repo'] = visit_repo
                data[name]['changelog'] = changelog
        except Exception:  # pylint: disable=W0703
            pass
    return data
