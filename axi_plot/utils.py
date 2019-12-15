import subprocess
import logging
import os, time
from pathlib import Path
from shutil import copyfile
import pandas as pd
from datetime import datetime

def estimate_time(filename, config, layer=None):
    base_commands = ['axicli', filename, '--config', config]
    end_command = ['-vTC']
    if layer is None:
        process = subprocess.run(base_commands+end_command, stdout=subprocess.PIPE, universal_newlines=True)
    else:
        commands = base_commands + ['--mode', 'layers', '--layer', str(layer)] + end_command
        process = subprocess.run(commands, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout

def plot(filename, config, checkpoint_file, layer=None):

    base_commands = ['axicli', filename, '--config', config]
    end_commands = ['-o', checkpoint_file]
    if layer is None:
        commands = base_commands + end_commands
    else:
        commands = base_commands + ['--mode', 'layers', '--layer', str(layer)] + end_commands

    process = subprocess.run(commands, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout

def res_plot(filename, config, checkpoint_file):
    """
    base_commands = ['axicli', filename, '--config', config, '--mode', 'res_plot']
    end_commands = ['-o', checkpoint_file]
    commands = base_commands + end_commands
    process = subprocess.run(commands, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout
    """
    raise Exception()


def toggle_pen(config):
    process = subprocess.run(['axicli', '-mtoggle', '--config', config], stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout

def return_home(filename):
    process = subprocess.run(['axicli', filename, '--mode', 'res_home'], stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout


def backup_drawing(file):
    """
    Check to see if $PLOTTER_BACKUP exists. If it does, then copy over the file
    if it doesnt exist, and add to the print logs that we are printing it.
    """
    if 'PLOTTER_BACKUP' in os.environ:
        logging.info("backing up {}".format(file))
        filename = os.path.basename(file)
        backup_dir = os.path.join(os.environ.get('PLOTTER_BACKUP'))
        backup_path = os.path.join(backup_dir, filename)
        if not os.path.exists(backup_path):
            copyfile(file, backup_path)

        print_logs = os.path.join(backup_dir, "print_logs.csv")
        if os.path.exists(print_logs):
            logs = pd.read_csv(print_logs)
        else:
            logs = pd.DataFrame({})

        df = pd.DataFrame([{'name':filename, 'time_printed':datetime.now().strftime('%Y-%m-%d %H:%M')}], columns=['name', 'time_printed'])
        logs = logs.append(df, sort=False)

        logs.to_csv(print_logs, index=False)

    else:
        logging.info("Skipping backup for {}, no $PLOTTER_BACKUP path given".format(file))

def get_checkpoint_file(file, tmp_folder="tmp"):
    filename = os.path.basename(file)
    tmp_dir = os.path.join(os.getcwd(), tmp_folder)
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)
    temp_file = os.path.join(tmp_dir, filename)
    logging.info("making tempfile {}".format(temp_file))

    now = time.time()
    # delete files older than a week
    for f in os.listdir(tmp_dir):
        if os.stat(os.path.join(tmp_dir, f)).st_mtime < now - 7 * 86400:
            os.remove(os.path.join(tmp_dir, f))

    return temp_file

def get_checkpoint_and_new_checkpoint(file, tmp_folder="tmp"):
    checkpoint = get_checkpoint_file(file, tmp_folder)
    active_checkpoint = "{}-active".format(checkpoint)
    os.rename(checkpoint, active_checkpoint)
    return active_checkpoint, checkpoint

def clean_tmp_file(file):
    try:
        os.remove(file)
    except:
        logging.warning("Could not delete temp file {}".format(file))

def get_config_names(config_folder = 'configs'):
    dir = os.path.join(os.getcwd(), config_folder)
    configs = []
    for file in os.listdir(dir):
        configs.append(os.path.basename(file))
    return configs

def get_full_config_path(config, config_folder = 'configs'):
    dir = os.path.join(os.getcwd(), config_folder)
    return os.path.join(dir, config)
