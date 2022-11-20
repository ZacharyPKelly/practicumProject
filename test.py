GITHUB_CLI_VERSION = '$(curl -s "https://api.github.com/repos/cli/cli/releases/latest" | grep -Po ' + "'" + '"tag_name": "v\K[0-9.]+' + "')"
print()
print(GITHUB_CLI_VERSION)
print()
print('"https://github.com/cli/cli/releases/latest/download/gh_' + GITHUB_CLI_VERSION + '_linux_armv6.deb"')