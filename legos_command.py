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
    gh = Github()
    ctx.obj['GITHUB'] = gh
    if ctx.invoked_subcommand is None:
        click.echo("Hello there!")

@cli.command(name='issues')
@click.pass_context
@click.option('--status', default='open', metavar='<text>', help='Indicates the state of the issues to return. Can be either open, closed, or all. Default: open')
@click.option('--repo', metavar='<github_repo>', help='lists the issues for the repo')
def list_issues(ctx, repo, status):
    ''' lists open issues for the repo by default'''
    
    if repo:
        repo_list = [repo]
    else:
        repo_list = get_tracked_repos()

    if repo_list.count == 0:
        click.echo("No tracked repo")
    
    gh = ctx.obj['GITHUB']

    for item in repo_list:
        click.echo(status + " issues from " + item)
        issues = gh.get_repo(item).get_issues(state=status)
        
        for issue in issues:
            localtiem = arrow.get(issue.created_at).to('local').humanize()
            click.echo("{:4d} {:55.55} {}".format(issue.number, issue.title, localtiem))

@cli.command(name='stats')
@click.option('--repo', metavar='<github_repo>', help='get stats for the repo')
@click.pass_context
def project_stats(ctx, repo):
    '''shows the basic project stats like stars, issues, watch and PRs for tracked/single repo'''
    print "\nProject stats"

    gh = ctx.obj['GITHUB']

    if repo is not None:
        print_stats(repo, gh)
        return
    
    repo_list = get_tracked_repos()
    for project in repo_list:
        print_stats(project, gh)

@cli.command(name='labels')
@click.option('--repo', metavar='<github_repo>', help='get labels stats for the repo')
@click.pass_context
def label_stats(ctx, repo):
    
    gh = ctx.obj['GITHUB']
    
    label_list = ['bug', 'feature', 'need-more-info']

    if repo is not None:
        mylabels = get_lables(gh.get_repo(repo), label_list)
        print_label_stats(repo, gh, mylabels)
        return
    
    repo_list = get_tracked_repos()
    
    for project in repo_list:
        mylabels = get_lables(gh.get_repo(project), label_list)
        print_label_stats(project, gh, mylabels)

def print_label_stats(repo, git, mylabels):
    project = git.get_repo(repo)
    for label in mylabels:
        issues = project.get_issues(state='open', labels = [label])
        print "label: {0}\tcount: {1}".format(label.name, total_count(issues))
    print "PRs: {0}".format(get_pr_count(project))
    

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

    repo_list = get_tracked_repos()

    if list or repo is None:
        for item in repo_list:
            print item
        return

    file = open(file_name,'a')
    if repo not in repo_list:
        file.write (repo+'\n')
        file.close()
    click.echo(repo+ ' is added to the list')

def get_tracked_repos():
    file_name = os.path.join(gettempdir(), 'repos.txt')
    file = open(file_name,'r')
    list_repo = map(lambda p: p.rstrip(), file.readlines())
    file.close()
    return list_repo

def print_stats(project, git):
    repo = git.get_repo(project)
    click.secho(repo.name, bold=True)
    click.echo(repo.description)
    pr_count = get_pr_count(repo)

    stats_text = "stars: {0}\tissues: {1}\twatch: {2}\tPRs: {3}\n".format(repo.stargazers_count, repo.open_issues_count, repo.watchers_count, pr_count)
    click.echo(stats_text)

def get_lables(repo, names):
    labels = []
    for name in names:
       labels.append(repo.get_label(name))
    return labels

def get_pr_count(repo):
    return total_count(repo.get_pulls(state='open'))

def total_count(paginated_list):
    pl_count = 0
    for _ in paginated_list:
        pl_count = pl_count + 1
    return pl_count

if  __name__ == '__main__':
    cli(obj={})