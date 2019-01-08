"""Create a new release for your repo."""
from github import Github
from github.GithubException import UnknownObjectException
from reporeleaser.const import (BODY, CHANGELOG, FOOTER, SEPERATOR,
                                RELEASETYPES, RELEASEURL)


class CreateRelease():
    """Class for release creation."""

    def __init__(self, token, repo, release, test, title, draft, show_sha,
                 hide_footer, hide_full_changelog):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.release = release
        self.test = test
        self.title = title
        self.draft = draft
        self.show_sha = show_sha
        self.hide_footer = hide_footer
        self.hide_full_changelog = hide_full_changelog
        self.github = Github(token)
        self.repo_obj = None
        self.first_release = False

    def create_release(self):
        """Create a new release for your repo."""
        if not self.release:
            print('--release was not defined')
            return

        self.repository()

        self.repo_object()
        if self.repo_obj is None:
            return

        last_commit = self.last_commit()
        if last_commit is None:
            return

        last_release = self.last_release()
        if last_release['tag_name'] is None:
            return

        if not last_release['tags']:
            if self.release not in RELEASETYPES:
                new_version = self.release
        else:
            new_version = self.new_version(last_release)

        if new_version is None:
            return

        description = self.release_description(last_release, new_version)

        if description is None:
            return

        if self.title is not None:
            title = self.title
        else:
            title = new_version

        if not self.test:
            self.publish(title, new_version, description, last_commit)
        else:
            print("Draft:", self.draft)
            print("Tag name:", new_version)
            print("Release title:", title)
            print("Release description:")
            print(SEPERATOR)
            print(description)
            print("Test mode was active skipping release.")

    def repository(self):
        """Set correct repository name."""
        if '/' not in self.repo:
            user = self.github.get_user().login
            self.repo = "{}/{}".format(user, self.repo)

    def repo_object(self):
        """Set repo object."""
        try:
            self.repo_obj = self.github.get_repo(self.repo)
        except UnknownObjectException:
            message = "Repository {} not found."
            print(message.format(self.repo))

    def last_commit(self):
        """Get last commit."""
        last_commit = None
        last_commit = self.repo_obj.get_branch(self.repo_obj.default_branch)
        last_commit = last_commit.commit.sha
        return last_commit

    def new_version(self, last_release):
        """Return new version."""
        major = 0
        minor = 0
        patch = 0

        if self.release not in RELEASETYPES:
            version = self.release
        else:
            if 'v' in last_release['tag_name']:
                current_version = last_release['tag_name'].split('v')[1]
                current_version = current_version.split('.')
            else:
                current_version = last_release['tag_name'].split('.')
            segments = len(current_version)

            if self.release == 'major':
                major = int(current_version[0]) + 1

            elif self.release == 'minor':
                major = current_version[0]
                minor = int(current_version[1]) + 1

            elif self.release == 'patch':
                major = current_version[0]
                minor = current_version[1]
                patch = int(current_version[2]) + 1

            if segments == 2:
                version = "{}.{}".format(major, minor)
            elif segments == 3:
                version = "{}.{}.{}".format(major, minor, patch)

            if 'v' in last_release['tag_name']:
                version = 'v' + version
        return version

    def last_release(self):
        """Return last release."""
        import re
        tag_sha = None
        data = {}
        tags = list(self.repo_obj.get_tags())
        reg = "(v|^)?(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$"
        if tags:
            data['tags'] = True
            for tag in tags:
                tag_name = tag.name
                if re.match(reg, tag_name):
                    tag_sha = tag.commit.sha
                    break
            if tag_sha is None:
                if self.release in RELEASETYPES:
                    tag_name = None
                    message = "Could not find a previous tag matching "
                    message += "(v)X.X(.X)"
                    print(message)
        else:
            data['tags'] = False
            tag_name = '0.0.1'
        data['tag_name'] = tag_name
        data['tag_sha'] = tag_sha
        return data

    def new_commits(self, sha):
        """Get new commits."""
        if sha is None:
            commits = self.repo_obj.get_commits()
        else:
            from datetime import datetime
            dateformat = "%a, %d %b %Y %H:%M:%S GMT"
            release_commit = self.repo_obj.get_commit(sha)
            since = datetime.strptime(release_commit.last_modified, dateformat)
            commits = self.repo_obj.get_commits(since=since)
        return list(commits)

    def release_description(self, last_release, version):
        """Create release description."""
        if self.release == 'initial':
            description = ':tada: Initial release of this repo :tada:\n'
            description += FOOTER
        else:
            description = BODY
            commits = self.new_commits(last_release['tag_sha'])
            if len(commits) - 1 == 0:
                print("There is no new commits to release.")
                return None
            for commit in reversed(commits):
                if commit.sha == last_release['tag_sha']:
                    pass
                else:
                    message = self.repo_obj.get_git_commit(commit.sha).message
                    message = message.split('\n')[0]
                    if self.show_sha:
                        line = "- {} {} \n".format(commit.sha[0:7], message)
                    else:
                        line = "- {}\n".format(message)
                    description += line
            if not self.hide_full_changelog:
                if last_release['tag_sha'] is not None:
                    description += "\n[Full Changelog][changelog]\n"
            description += "\n"
            if not self.hide_footer:
                description += FOOTER
            if not self.hide_full_changelog:
                if last_release['tag_sha'] is not None:
                    changelog = CHANGELOG.format(self.repo,
                                                 last_release['tag_name'],
                                                 version)
                    description += changelog
        return description

    def publish(self, title, new_version, description, last_commit):
        """Publish the release."""
        try:
            self.repo_obj.create_git_tag_and_release(new_version, '',
                                                     title, description,
                                                     last_commit, '',
                                                     draft=self.draft)
            if self.draft:
                print("The release draft was created.")
            else:
                print("The release was published.")
            print(RELEASEURL.format(self.repo, new_version))
        except UnknownObjectException:
            message = "You do not have premissions to push to {}"
            print(message.format(self.repo))
        except Exception as error:  # pylint: disable=W0703
            print("Something went horrible wrong :(")
            print(error)
