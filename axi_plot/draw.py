import click
import logging

from axi_plot import utils

LINE_SEPERATOR = "-------------------------------------------"

def set_logging(verbose):
    logging.basicConfig()
    if verbose == 0:
        logging.getLogger().setLevel(logging.WARNING)
    elif verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif verbose > 1:
        logging.getLogger().setLevel(logging.DEBUG)

@click.argument('filename', type=click.Path(exists=True))
@click.command()
def return_home(filename):
    temp_file = utils.get_checkpoint_file(filename)
    utils.return_home(temp_file)


@click.argument('filename', type=click.Path(exists=True))
@click.option('--config', type=click.Choice(utils.get_config_names(), case_sensitive=False), default="ems_default.py")
@click.command()
def resume(filename, config):
    temp_file = utils.get_checkpoint_file(filename)
    source, output = utils.get_checkpoint_and_new_checkpoint(filename)
    utils.res_plot(source, config, output)

def calibrate_pens(config):
    while not click.confirm('Done with pen calibration?', default=False):
        utils.toggle_pen(config)


@click.argument('filename', type=click.Path(exists=True))
@click.option('--config', type=click.Choice(utils.get_config_names(), case_sensitive=False), default="ems_default.py")
@click.option("-v", "--verbose", default = 1, count=True)
@click.option('-l', '--layer', required=False, type=int, multiple=True)
#reordering
@click.command()
def draw(filename, config, verbose, layer):

    set_logging(verbose)

    config = utils.get_full_config_path(config)
    logging.info("Using config {}".format(config))

    filename = click.format_filename(filename)
    temp_file = utils.get_checkpoint_file(filename)
    utils.backup_drawing(filename)

    if layer:
        for l in layer:
            click.echo("Estimated Time to plot for layer {}".format(l))
            click.echo(LINE_SEPERATOR)
            click.echo(utils.estimate_time(filename, config, layer=l))

        for l in layer:
            click.echo(LINE_SEPERATOR)
            click.echo("Processing layer {}".format(l))
            calibrate_pens(config)
            utils.plot(filename, config, temp_file, layer=l)
    else:
        click.echo("Estimated Time to plot")
        click.echo(LINE_SEPERATOR)
        click.echo(utils.estimate_time(filename, config))
        calibrate_pens(config)
        utils.plot(filename, config, temp_file, layer=None)

    #utils.clean_tmp_file(temp_file)
