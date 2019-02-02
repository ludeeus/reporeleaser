"""Create a new release for your repo."""
from github import Github
from github.GithubException import UnknownObjectException
from reporeleaser.const import (BODY, CHANGELOG, FOOTER, RELEASETYPES,
                                RELEASEURL)
from reporeleaser.messages import (RELEASE_MISSING, NO_PREVIOUS_RELEASE,
                                   TEST_MODE, REPOSITORY_NOT_FOUND,
                                   SEGMENT_PATCH_MISSING, DRAFT_CREATED,
                                   RELEASE_PUBLISHED, PERMISSION_ERROR,
                                   GENERIC_ERROR, NO_NEW_COMMITS,
                                   NO_MATCHING_TAG)


class CreateRelease():
    """Class for release creation."""

    def __init__(self, token, repo, release, test, title, draft, prerelease,
                 show_sha, show_author, hide_footer, hide_full_changelog):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.release = release
        self.test = test
        self.title = title
        self.draft = draft
        self.prerelease = prerelease
        self.show_sha = show_sha
        self.show_author = show_author
        self.hide_footer = hide_footer
        self.hide_full_changelog = hide_full_changelog
        self.github = Github(token)
        self.repo_obj = None
        self.first_release = False

    def create_release(self):
        """Create a new release for your repo."""
        if not self.release:
            print(RELEASE_MISSING)
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
                new_version = None
                print(NO_PREVIOUS_RELEASE)
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
            print(TEST_MODE.format(draft=self.draft,
                                   prerelease=self.prerelease,
                                   tag=new_version, title=title,
                                   description=description))

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
            print(REPOSITORY_NOT_FOUND.format(self.repo))

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
                if segments == 3:
                    major = current_version[0]
                    minor = current_version[1]
                    patch = int(current_version[2]) + 1
                else:
                    version = None
                    previous_tag = last_release['tag_name']
                    print(SEGMENT_PATCH_MISSING.format(previous_tag))
                    return version

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
                    print(NO_MATCHING_TAG)
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
                print(NO_NEW_COMMITS)
                return None
            for commit in reversed(commits):
                if commit.sha == last_release['tag_sha']:
                    pass
                else:
                    message = self.repo_obj.get_git_commit(commit.sha).message
                    message = message.split('\n')[0]
                    line = '- '
                    if self.show_sha:
                        line += "{} ".format(commit.sha[0:7])
                    line += "{} ".format(message)
                    if self.show_author:
                        line += "@{} ".format(commit.author.login)
                    line += '\n'
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
            prerelease = self.prerelease
            self.repo_obj.create_git_tag_and_release(new_version, '',
                                                     title, description,
                                                     last_commit, '',
                                                     draft=self.draft,
                                                     prerelease=prerelease)
            if self.draft:
                print(DRAFT_CREATED)
                print(RELEASEURL.format(self.repo, '', ''))
            else:
                print(RELEASE_PUBLISHED)
                print(RELEASEURL.format(self.repo, '/tag/', new_version))
        except UnknownObjectException:
            print(PERMISSION_ERROR.format(self.repo))
        except Exception as error:  # pylint: disable=W0703
            print(GENERIC_ERROR.format(error))
