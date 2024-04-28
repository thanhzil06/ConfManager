import os
import json
import logging.config


class LoadLogconf:
    def __init__(self, logger_choice, output_path=""):
        self.output_folder = output_path
        try:
            if output_path == "":
                os.mkdir("../logs")
            else:
                os.mkdir(os.path.join(output_path, "logs"))
        except FileExistsError as FolderIssue:
            pass
        self.logger_choice = logger_choice
        self._setup_logging(logger=self.logger_choice)

    def _setup_logging(self, default_path="\\logging.json", env_key="LOG_CFG",
                       logger="dev"):
        """
        Setup logging configuration
        """
        path = default_path
        value = os.getenv(env_key, None)
        dir_path = os.path.dirname(__file__)
        fpath = str(dir_path) + path
        if value:
            fpath = value
        if os.path.exists(fpath):
            with open(fpath, 'rt') as f:
                config = json.load(f)
                for handler in config["handlers"]:
                    if 'filename' in config['handlers'][handler].keys():
                        logfile = config['handlers'][handler]['filename']
                        config['handlers'][handler]['filename'] = os.path.join(self.output_folder, "logs", logfile)
            logging.config.dictConfig(config)
        self.log = logging.getLogger(logger)

    def get_logger(self):
        return self.log
