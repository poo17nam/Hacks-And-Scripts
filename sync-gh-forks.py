#!/usr/bin/python3
# coding=utf-8


from subprocess import call, check_output

import requests

if __name__ == '__main__':
    """
       Run a bunch of boilerplate commands to sync your local clone to its
       parent github repo.
    """
    print("Starting sync...", "\n")

    CURRENT_REPO_ORIGIN = ['git', 'config', '--get', 'remote.origin.url']
    CURRENT_REPO_UPSTREAM = ['git', 'config', '--get', 'remote.upstream.url']
    ADD_REMOTE_CMD = ['git', 'remote', 'add', 'upstream']
    CHECK_REMOTES_CMD = ['git', 'remote', '-v']
    FETCH_UPSTREAM_CMD = ['git', 'fetch', 'upstream']
    CHECKOUT_MASTER_CMD = ['git', 'checkout', 'master']
    MERGE_UPSTREAM_CMD = ['git', 'merge', 'upstream/master']
    PUSH_TO_UPSTREAM_CMD = ['git', 'push', 'origin', 'master']

    try:
        repo_origin_url = str(check_output(CURRENT_REPO_ORIGIN))
        repo_origin_url = repo_origin_url.replace("\n", "")

        repo_upstream_url = str(check_output(CURRENT_REPO_UPSTREAM))

        print("Getting repo's url...")
        print("Syncing repo:", repo_origin_url)

        print("Fetching upstream...", "\n")
        call(FETCH_UPSTREAM_CMD)
        print("")

        print("Merging upstream and master", "\n")
        call(CHECKOUT_MASTER_CMD)
        call(MERGE_UPSTREAM_CMD)
        print("Syncing done.")

        print("Pushing to origin master", "\n")
        call(PUSH_TO_UPSTREAM_CMD)
        print("Push done.")

    except Exception as e:
        repo_origin_url = str(check_output(CURRENT_REPO_ORIGIN))
        repo_origin_url = repo_origin_url.replace("\n", "")

        print("Getting repo's url...")
        print("Syncing repo:", repo_origin_url)

        if repo_origin_url[0] == "h":
            url_segments = repo_origin_url.split("https://github.com/")

        if repo_origin_url[0] == "g":
            url_segments = repo_origin_url.split("git@github.com:")

        path = url_segments[1]
        user, repo = path.split("/")
        repo = repo.replace(".git", "")
        print(user, repo)

        print("Getting upstream url for the repo ...", "\n")
        url = "https://api.github.com/repos/{}/{}".format(user, repo)
        response = requests.get(url)
        repo_upstream_url = response.json()["parent"]["clone_url"]

        print("Upstream URL is:-", repo_upstream_url)

        ADD_REMOTE_CMD.append(repo_upstream_url)
        print(ADD_REMOTE_CMD)

        print("Upstream is added to the fork", "\n")
        call(ADD_REMOTE_CMD)
        print("")

        print("Fetching upstream...", "\n")
        call(FETCH_UPSTREAM_CMD)
        print("")

        print("Merging upstream and master", "\n")
        call(CHECKOUT_MASTER_CMD)
        call(MERGE_UPSTREAM_CMD)
        print("Syncing done.")

        print("Pushing to origin master", "\n")
        call(PUSH_TO_UPSTREAM_CMD)
        print("Push done.")
