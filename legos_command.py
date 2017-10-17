import click
import arrow
import os
from tempfile import gettempdir
from github import Github

@click.group()
@click.pass_context
def cli(ctx):
    '''This is a command line tool to list the github issues'''
    #TODO: add code to fetch issue details
    click.echo("Hello there!")

@cli.command(name='list')
@click.pass_context
@click.option('--status', default='open', metavar='<text>', help='Indicates the state of the issues to return. Can be either open, closed, or all. Default: open')
@click.argument('repo', metavar='<github_repo>')
def list_issues(ctx, repo):
    ''' lists open issues for the repo by default'''
    gh = Github()
    
    click.echo(status+" issues from " + repo)
    for issue in gh.get_repo(repo).get_issues(state=status):
        localtiem = arrow.get(issue.created_at).to('local').humanize()
        click.echo("{:4d} {:55.55} {}".format(issue.number, issue.state, localtiem))

@cli.command(name='track')
@click.option('--repo', metavar='<github_repo>', help='add the repo to the trac list')
@click.option('--list', is_flag=True, help='Lists all tracked repos')
@click.pass_context
def add_repo(ctx, repo, list):
    '''adds the repo to the tracking list'''
    
    file_name = os.path.join(gettempdir(), 'repos.txt')
    if not os.path.exists(file_name):
        file = open(file_name, 'w')
        if repo:
            file.write(repo + '\n')
        file.close

    file = open(file_name,'r+')
    list_repo = map(lambda p: p.rstrip(), file.readlines())

    if list:
        for item in list_repo:
            print item
        return

    if repo not in list_repo:
        file.write(repo+'\n')
        file.close()
    click.echo(repo+ ' is added to the list')

if  __name__ == '__main__':
    cli(obj={})