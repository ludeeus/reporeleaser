"""Default values."""
BODY = "## Changes\n\n"
CHANGELOG = "[changelog]: https://github.com/{}/compare/{}...{}"
FOOTER = """***

This release was created with [reporeleaser][reporeleaser] :tada:

[reporeleaser]: https://pypi.org/project/reporeleaser/
"""
GITLAB_CI_BADGE = "[![GitLab CI][gitlabci-shield]][gitlabci]\n\n"
GITLAB_CI_BADGE_LINKS = """
[gitlabci-shield]: https://gitlab.com/{}/badges/{}/pipeline.svg
[gitlabci]: https://gitlab.com/{}/pipelines
"""
RELEASETYPES = ['major', 'minor', 'patch', 'beta']
RELEASEURL = "https://github.com/{}/releases{}{}"
