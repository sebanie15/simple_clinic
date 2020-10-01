"""Console script for simple_clinic."""
import sys
import click


class ActiveDoctor(object):

    def __init__(self):
        self.id = 0


active = click.make_pass_decorator(ActiveDoctor, ensure=True)


@click.group()
@click.option('--id', type=int, help='')
@active
def cli(active, id):
    """Console script for simple_clinic."""
    active.id = id
    return 0


@cli.command()
@active
def show_activated(active):
    click.echo(f'Activated = {active.id}')
    # click.echo(f'activated : {activated}')


@cli.command()
@click.option('--set_id', type=int)
@active
def set_activated(active, set_id):
    active.id = set_id


@cli.command()
@active
def print_test(active):
    print(active.id)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
