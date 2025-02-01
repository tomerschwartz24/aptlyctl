import typer
from rich import print
from cli import list_repos, show_repo, create_repo

app = typer.Typer(name="aptlyctl")

@app.command()
def repos_list():
    """
    list all repositories within aptly remote server
    """
    list_repos()
    

@app.command()
def repo_show(repo_name: str):
    """
    get information about a specific repository, e.g "aptlyctl repo-show great-repository"
    """
    repo_data = show_repo(repo_name)
    print(repo_data) 

@app.command()
def repo_create(repo_name: str, comment: str = "", default_distribution: str = "", default_component: str = "", from_snapshot: str = ""):
    """
    create a repository, Required parameters : repo_name , Optional parameters: [comment, default_distribution, default_component, from_snapshot]
    """
    creation_attempt = create_repo(repo_name, comment, default_distribution, default_component, from_snapshot)
    print(creation_attempt)

@app.callback()
def show_help(ctx: typer.Context):
    if not ctx.invoked_subcommand:
        print("No command provided. Use --help to list available commands.")
        ctx.exit()
    
if __name__ == '__main__':
    app()