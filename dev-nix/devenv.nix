{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;

    venv.enable = true;
    venv.requirements = ''
      psutil
      mysql-connector-python
      python-dotenv
      tabulate
      numpy
      pandas
    '';
  };
}