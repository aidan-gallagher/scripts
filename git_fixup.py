#!/usr/bin/env python3

# Gitlint (https://jorisroovers.com/gitlint/) can be used on pull request checks to ensure good git message quality.
# If you have a lot of simple git lint errors it can be boring to manually resolve them.
# This script aims to automate some of the fixes.

import sys
import git_filter_repo


def add_jira_ticket(commit, _):
	"""" If commit doesn't have a jira ticket already then add one """
	# Get Jira ticket
	if len(sys.argv) < 3:
		raise Exception('Please supply jira number as an argument')
	else:
		jira_id     = sys.argv[2]
		jira_prefix = jira_id.split('-')[0]

	# Add Jira ticket to commit
	msg = commit.message.decode("utf-8")
	if jira_prefix not in msg:
		msg = msg + "\n" + jira_id
		
	commit.message = msg.encode("utf-8")


def remove_trailing_full_stop(commit, _):
	"""Remove full stop from git title."""
	msg = commit.message.decode("utf-8")

	# Remove full stop from title if it contains one.
	title = msg.partition('\n')[0]
	if title[-1] == ".":
			title = title[:-1]
	
	# Generate new commit message (new_msg).
	new_msg = title
	for line in msg.partition('\n')[1:]:
		new_msg += line

	commit.message = new_msg.encode("utf-8")
		
if __name__ == "__main__":
	"Ensure all changes are stashed or committed before running"

	if len(sys.argv) < 2:
		raise Exception('Please choose a function')
	else:
		if sys.argv[1] == "add_jira":
			func = add_jira_ticket
		elif sys.argv[1] == "remove_fullstop":
			func = remove_trailing_full_stop

	# Run git-filter-repo
	args = git_filter_repo.FilteringOptions.default_options()
	args.force = True
	args.refs = ['master..HEAD']
	git_filter_repo.RepoFilter(
		args,
		commit_callback=func
	).run()
