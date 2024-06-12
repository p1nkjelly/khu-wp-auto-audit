## installation
```sh
./install_progpilot.sh
```

php 7.4+ is needed for progpilot.

## run
```sh
ln -s {plugins_dir} plugins
mkdir results
./progpilot.py
```

## configuration
- `plugin_path`: directory path of wordpress plugins
- `save_path`: directory path of scanning results
- `analysis_file`: php file created by python script
