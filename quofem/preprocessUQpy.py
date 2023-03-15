import click
import os


@click.command()
@click.option('--workflowInput', type=click.Path(exists=True, readable=True), required=True,
              help="Path to JSON file containing the details of FEM and UQ tools.")
@click.option('--driverFile', type=click.Path(exists=True, readable=True),
              help="ASCII file containing the details on how to run the FEM application.")
@click.option('--runType', type=click.Choice(['runningLocal', 'runningRemote']),
              default='runningLocal', help="Choose between local or cluster execution of workflow.")
@click.option('--osType', type=click.Choice(['Linux', 'Windows']),
              help="Type of operating system the workflow will run on.")
def preprocess(workflowinput, driverfile, runtype, ostype):
    pass


if __name__ == "__main__":
    preprocess()
