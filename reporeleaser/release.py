"""Create a new release for your repo"""
from github import Github
from github.GithubException import UnknownObjectException
from reporeleaser.const import BODY, FOOTER, SEPERATOR, RELEASETYPES, VERSION


class CreateRelease():
    """Class for release creation."""

    def __init__(self, token, repo, release_type, test):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.release_type = release_type
        self.test = test
        self.github = Github(token)

    def release(self):
        """Create a new release for your repo."""
        first_release = False
        repo = self.github.get_repo(self.repo)
        commits = list(repo.get_commits())
        tags = list(repo.get_tags())
        last_commit = commits[0].sha
        prev_tag = None
        prev_tag_sha = None
        body = BODY
        if tags:
            for tag in tags:
                prev_tag = tag.name
                prev_tag_sha = tag.commit.sha
                if not 'untagged' in prev_tag:
                    break
        else:
            first_release = True


        if first_release:
            if self.release_type not in RELEASETYPES:
                version = self.release_type
            else:
                version = '0.0.1'
        else:
            if self.release_type not in RELEASETYPES:
                version = self.release_type
            else:
                if 'v' in prev_tag:
                    curr_version = prev_tag.split('v')[1].split('.')
                else:
                    curr_version = prev_tag.split('.')
                if self.release_type == 'major':
                    major = curr_version[0] + 1
                    minor = curr_version[1]
                    patch = curr_version[2]
                    version = VERSION.format(major, minor, patch)
                elif self.release_type == 'minor':
                    major = curr_version[0]
                    minor = curr_version[1] + 1
                    patch = curr_version[2]
                    version = VERSION.format(major, minor, patch)
                elif self.release_type == 'patch':
                    major = curr_version[0]
                    minor = curr_version[1]
                    patch = curr_version[2] + 1
                    version = VERSION.format(major, minor, patch)
                if 'v' in prev_tag:
                    version = 'v' + version
        for commit in list(repo.get_commits()):
            if not first_release:
                if commit.sha == prev_tag_sha:
                    break

            body = body + '- ' + repo.get_git_commit(commit.sha).message + '\n'

        body = body + FOOTER


        if not self.test:
            try:
                repo.create_git_tag_and_release(version,
                                                '',
                                                version,
                                                body,
                                                last_commit,
                                                '')
            except UnknownObjectException:
                message = "You do not have premissions to push to {}"
                print(message.format(self.repo))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print("Version", version)
            print("Body:")
            print(SEPERATOR)
            print(body)
            print("Test was enabled, skipping release")
