"""Generate json form custom-components org."""
from reporeleaser.defaults import REUSE, VISIT, SKIP_REPOS


def get_data(github, selected_repos):
    """Generate json form custom-components org."""
    org = 'custom-components'
    data = {}
    repos = []
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        repo = github.get_repo(org + '/' + repo)
        if repo.name not in SKIP_REPOS and not repo.archived:
            print("Generating json for repo:", repo.name)
            name = repo.name
            updated_at = repo.updated_at.isoformat().split('T')[0]
            if len(name.split('.')) > 1:
                location = 'custom_components/{}/{}.py'
                location = location.format(name.split('.')[0],
                                           name.split('.')[1])
            else:
                location = 'custom_components/{}.py'.format(name)
                try:
                    repo.get_file_contents(location)
                except Exception:  # pylint: disable=W0703
                    location = 'custom_components/{}/__init__.py'
                    location = location.format(name)

            version = None
            try:
                content = repo.get_file_contents(location)
                content = content.decoded_content.decode().split('\n')
                for line in content:
                    if '_version_' in line or 'VERSION' in line:
                        version = line.split(' = ')[1].replace("'", "")
                        break
            except Exception:  # pylint: disable=W0703
                version = None

            try:
                releases = list(repo.get_releases())
                changelog = releases[0].html_url
                if 'untagged' in changelog:
                    changelog = releases[1].html_url
                if 'untagged' in changelog:
                    changelog = VISIT.format(org, name)
            except Exception:  # pylint: disable=W0703
                changelog = VISIT.format(org, name)

            updated_at = updated_at
            version = version
            local_location = '/{}'.format(location)
            remote_location = REUSE.format(org, name, location)
            visit_repo = VISIT.format(org, name)
            changelog = changelog

            data[name] = {}
            data[name]['updated_at'] = updated_at
            data[name]['version'] = version
            data[name]['local_location'] = local_location
            data[name]['remote_location'] = remote_location
            data[name]['visit_repo'] = visit_repo
            data[name]['changelog'] = changelog
    return data
