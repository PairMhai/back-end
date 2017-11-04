from django.conf import settings
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView


from github import GithubException
from github.GithubException import RateLimitExceededException

from utilities.classes.library import ImpGithub

# Create your views here.


class Index(APIView):

    def get_github_status(self, github):
        id = github.get_backend().id
        html_url = github.get_backend().html_url
        homepage = github.get_backend().homepage
        last_update = github.get_backend().updated_at
        size = github.get_backend().size
        # tags = self.get_backend().get_tags()
        releases = github.get_backend().get_releases()

        latest_event = github.get_backend().get_network_events()[0]

        stat_commit = github.get_backend().get_stats_commit_activity()

        # return_tags = []
        return_releases = []

        # for tag in tags:
        # return_tags.append(tag.name)

        # only 2 latest version
        for release in releases[0:2]:
            return_releases.append(
                "{} --> ({})".format(release.title, release.tag_name))

        return {
            "id": id,
            "repository-location": html_url,
            "production-location": homepage,
            "size": size,
            "releases": return_releases,
            "latest-event": {
                "type": latest_event.type,
                # "payload": latest_event.payload,
                "actor": {
                    "login": latest_event.actor.login,
                    "email": latest_event.actor.email,
                    "url": latest_event.actor.html_url
                },
                "created_at": latest_event.created_at
            },
            "latest-update": last_update,
        }

    def get(self, request, format=None):
        github = ImpGithub() # "kamontat", "password"

        try:
            return Response({
                "api-version": settings.VERSION,
                "rate-status": github.get_rate_limiting(),
                "github-status": self.get_github_status(github),
            })
        except RateLimitExceededException as e:
            return Response({
                "status": e.status,
                "detail": e.data,
                "rate-limiting": github.get_rate_limiting()
            })
        except GithubException as e:
            return Response({
                "status": e.status,
                "detail": e.data
            })
