import click
import arrow
import os
from tempfile import gettempdir
from github import Github

@click.command()
@click.option("--list", is_flag=True, help='This will list all the open issue for a repo')
@click.option('--status', default='open', metavar='<text>', help='Indicates the state of the issues to return. Can be either open, closed, or all. Default: open')
@click.option('--track', is_flag=True)
@click.argument('repo', metavar='<github_repo>')
def cli(list,status,repo, track):
    '''This is a command line tool to list the github issues
    USAGE:
    
        legos <username/repo_name>
    '''

    if track:
        add_repo(repo)
        click.echo(repo+ ' is added to the list')
        return

    gh = Github()

    user = gh.get_user()

    click.echo(gh.get_rate_limit())

    click.echo(status+" issues from " +repo)
    for issue in gh.get_repo(repo).get_issues(state=status):
        localtiem = arrow.get(issue.created_at).to('local').humanize()
        click.echo("{:4d} {:55.55} {}".format(issue.number, issue.state, localtiem))

def add_repo(repo):
    file_name = os.path.join(gettempdir(), 'repos.txt')
    if not os.path.exists(file_name):
        file = open(file_name, 'w')
        file.write(repo + '\n')
        file.close
        return

    file = open(file_name,'r+')
    list_repo = map(lambda p: p.rstrip(), file.readlines())
    if repo not in list_repo:
        file.write(repo+'\n')
        file.close()

if  __name__ == '__main__':
    cli()