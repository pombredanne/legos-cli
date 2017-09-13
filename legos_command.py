import click
import arrow
from github import Github

@click.command()
@click.option("--list", is_flag=True, help='This will list all the open issue for a repo')
@click.argument('repo')
def cli(list, repo):
    '''This is a command line tool to list the github issues
    
    USAGE:
    
        legos <username/repo_name>
    '''
    
    gh = Github()

    for issue in gh.get_repo(repo).get_issues():
        localtiem = arrow.get(issue.created_at).to('local').humanize()
        print("{:4d} {:55.55} {}".format(issue.number, issue.title, localtiem))