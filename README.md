# Code Climate Bandit Engine

Code Climate Engine to run [Bandit](https://github.com/PyCQA/bandit).

Bandit is a tool designed to find common security issues in Python code.

## Installation

```
git clone https://github.com/noqcks/codeclimate-bandit
cd codeclimate-bandit
make release
```

## Usage

.codeclimate.yml
```
plugins:
  bandit:
    enabled: true
```

And then run the engine:

```
codeclimate analyze
```

## Configuration

The engine supports the native config file for Bandit. You can select the specific test plugins to run and override default Bandit configuration using this file. More information on the config file can be found in the [Bandit documentation](https://docs.openstack.org/bandit/latest/config.html).

A `.bandit.yaml` included at the root of your project will be included during engine run.

Example `.bandit.yaml`:

```
skips: ['B101', 'B601', 'B404']
```

## TODO

- support different locations of .bandit.yaml
