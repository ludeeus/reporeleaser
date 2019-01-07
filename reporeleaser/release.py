"""Create a new release for your repo."""
from github import Github
from github.GithubException import UnknownObjectException
from reporeleaser.const import (BODY, CHANGELOG, FOOTER, SEPERATOR,
                                RELEASETYPES, VERSION)


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
        if not self.release_type:
            print('--release_type was not defined, activating test mode.')
            self.test = True
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
                if 'untagged' not in prev_tag:
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
                    major = int(curr_version[0]) + 1
                    minor = curr_version[1]
                    patch = curr_version[2]
                    version = VERSION.format(major, minor, patch)
                elif self.release_type == 'minor':
                    major = curr_version[0]
                    minor = int(curr_version[1]) + 1
                    patch = curr_version[2]
                    version = VERSION.format(major, minor, patch)
                elif self.release_type == 'patch':
                    major = curr_version[0]
                    minor = curr_version[1]
                    patch = int(curr_version[2]) + 1
                    version = VERSION.format(major, minor, patch)
                if 'v' in prev_tag:
                    version = 'v' + version
        if version == '0.0.1' or version == 'v0.0.1':
            body = ':tada: Initial release of this repo :tada:'
            body = body + FOOTER
        else:
            for commit in list(repo.get_commits()):
                if not first_release:
                    if commit.sha == prev_tag_sha:
                        break
                message = repo.get_git_commit(commit.sha).message
                message = message.split('\n')[0]
                body = body + '- ' + message + '\n'
            body = body + "[Full Changelog][changelog]\n"
            body = body + FOOTER
            changelog = CHANGELOG.format(self.repo, prev_tag, version)
            body = body + changelog
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
            print("Test mode was active skipping release.")
