"""Messages uesd in prints."""
RELEASE_PUBLISHED = "The release was published."

DRAFT_CREATED = "The release draft was created."

NO_NEW_COMMITS = "There is no new commits to release."

NO_MATCHING_TAG = """
Could not find a previous tag matching the expected format.

                  (v)X.X(.X)
"""

GENERIC_ERROR = """
Something went horrible wrong :(
----------------------------------------------------------------------
{}
----------------------------------------------------------------------
"""

PERMISSION_ERROR = """
You do not have permissions to create a release for {}

Info: https://github.com/ludeeus/reporeleaser#option---token
"""

RELEASE_MISSING = """
Option '--release' was not defined.

Example: 'reporeleaser --token aabb1122 --repo reporeleaser --release minor'

Info: https://github.com/ludeeus/reporeleaser#option---release
"""

NO_PREVIOUS_RELEASE = """
No previous tag found, please use a custom release.

Example: 'reporeleaser --token aabb1122 --repo reporeleaser --release minor'

Info: https://github.com/ludeeus/reporeleaser#option---release
"""

TEST_MODE = """
Draft:         {draft}
Pre release:   {prerelease}
Tag name:      {tag}
Release title: {title}
Release description:
----------------------------------------------------------------------
{description}
----------------------------------------------------------------------
Test mode was active, the release was not published.

Info: https://github.com/ludeeus/reporeleaser#option---test
"""

REPOSITORY_NOT_FOUND = """
Repository {} was not found.

Info: https://github.com/ludeeus/reporeleaser#option---repo
"""


SEGMENT_PATCH_MISSING = """
You used `--release patch`, but the previous tag had not this segment.

Previous tag '{}'

Try using `--release minor` instead,

Info: https://github.com/ludeeus/reporeleaser#option---release
"""
