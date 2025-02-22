import typer
from rich import print
from cli import list_repos, show_repo, show_repo_packages, create_repo, delete_repo ,upload_single_file_to_aptly_upload_dir, upload_entire_deb_folder_to_upload_dir

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
def repo_packages_show(
                repo_name: str,
                package_name: str = typer.Option("", help="package name to query for") ,
                details: bool = typer.Option(False, "--details", help="Get verbose details about all packages or a single package"),
                with_deps: bool = typer.Option(False , "--with-deps",help="describe package dependencies (only relevant when querying a specific package)")
                ):
    """
    get package/s details, get package/s extended details, get package with its dependencies and extended details.
    """

    show_repo_packages(repo_name, package_name, details, with_deps)



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

#describing package dependencies is only relevant when querying a specific package
@app.command()
def repo_delete(repo_name: str,
                 force: bool = typer.Option(False, "--force", help="Force delete the repository if it has snapshots.")
                ):
    """
    delete a local repository (if repository is published it cannot be deleted, if repository has snapshot deletion must be forced.)
    """
    if force:
        force=1
    else:
        force=0
    deletion_attempt = delete_repo(repo_name, force=force)
    print(deletion_attempt)
@app.command()
def single_to_upload_dir(repo_name: str = typer.Argument(help="repository name to upload to (upload/repo_name/file will be created on the server)"), 
                       filepath: str = typer.Argument(help="Full Path to file you want to upload")
                ):
    """
    Upload a single deb file to aptly server (upload dir)
    """
    upload_single_file_to_aptly_upload_dir(repo_name, filepath)
    
@app.command()
def entire_dir_to_upload_dir(repo_name: str = typer.Argument(help="repository name to upload to (upload/repo_name/ will be created on the server)"), 
                       local_deb_dir: str = typer.Argument(help="Full Path to the local deb files dir you want to upload [e.g : /mnt/c/Users/tomer/work/debs/]")
                ):
    """
    Upload entire deb files directory to aptly server (upload dir)
    """
    upload_entire_deb_folder_to_upload_dir(repo_name, local_deb_dir)

@app.callback()
def show_help(ctx: typer.Context):
    if not ctx.invoked_subcommand:
        print("No command provided. Use --help to list available commands.")
        ctx.exit()
    
if __name__ == '__main__':
    app()