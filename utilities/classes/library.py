class ImpGithub():
    github = None

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def get_github(self):
        from github import Github

        if self.github is None:
            self.github = Github(self.username, self.password)
        return self.github

    def get_pairmhai(self):
        return self.get_github().get_organization("pairmhai")  # return Organization

    def get_backend(self):
        return self.get_pairmhai().get_repo("Backend")  # return Repository

    def get_rate_limiting(self):
        remain, limit = self.get_github().rate_limiting
        from datetime import datetime

        timestamp = self.get_github().rate_limiting_resettime
        date_time = datetime.fromtimestamp(timestamp)
        real_time = datetime.strftime(date_time, '%d/%m/%Y %H:%M:%S:%f')

        return {
            "rate_remaining": remain,
            "rate_limiting": limit,
            "rate_reset_time": real_time
        }
