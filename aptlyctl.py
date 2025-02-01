import typer
from rich import print
from cli import list_repos, show_repo, create_repo, upload_single_file_to_aptly

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
def repo_create(repo_name: str,
                comment: str = typer.Option("", help="text describing local repository, for the user"),
                default_distribution: str = typer.Option("", help="default distribution when publishing from this local repo") ,
                default_component: str = typer.Option("", help="default component when publishing from this local repo"),
                from_snapshot: str = typer.Option("", help="snapshot name to create repo from")
                ):
    """
    create a repository on remote aptly server
    """
    creation_attempt = create_repo(repo_name, comment, default_distribution, default_component, from_snapshot)
    print(creation_attempt)

@app.command()
def upload_single_file(repo_name: str = typer.Argument(help="repository name to upload to (upload/repo_name/file will be created on the server)"), 
                       filepath: str = typer.Argument(help="Full Path to file you want to upload")
                ):
    """
    Upload a deb file to aptly server (upload dir)
    """
    upload_single_file_to_aptly(repo_name, filepath)

@app.callback()
def show_help(ctx: typer.Context):
    if not ctx.invoked_subcommand:
        print("No command provided. Use --help to list available commands.")
        ctx.exit()
    
if __name__ == '__main__':
    app()