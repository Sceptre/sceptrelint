# sceptrelint
This repo contains scripts for the purpose of pre-commit processing
(e.g. linting) of [Sceptre configs](https://docs.sceptre-project.org/dev/docs/stack_config.html)

## Installation

The linter scripts can be installed by running `pip install .` and can be run from the
[sceptre project root directory](https://sceptre.cloudreach.com/dev/docs/templates.html#templates).

## Linters

* `check-file-names`  Checks that the value  of the `stack_name` matches the
file name (minus `.yaml`).

```yaml
-   id: check-file-names
```

* `check-stack-names` Checks for valid stack names in templates. Valid
stack names are [constraints specified by
CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html)

```yaml
-   id: check-stack-names
```

* `check-stack-tags` Checks that specific stack tags are defined.

The below checks that the `CostCenter` and `Project` tags are defined in sceptre
config's `stack_tags` key.
```yaml
-   id: check-stack-tags
    args: [--tag=CostCenter, --tag=Project]
```

* `check-stack-tag-values` Checks that a specific stack tag is assigned a valid value.


| args    | Description                                                                                                                                                |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tag     | The tag to validate                                                                                                                                        |
| file    | A json file with a list of valid tag values, can take a local or a url reference (i.e. https://raw.githubusercontent.com/acme/repo/master/valid_tags.json) |
| exclude | A tag to exclude from the valid list of tags                                                                                                               |

__Notes__:
 * The `file` and `exclude` args can be use multiple times
 * Example of a file containing valid tags values (valid_tags.json):
```
[
  "Engineering",
  "Operations",
  "Marketing",
  "Science"
]
```

__Example 1__: Checks that the `CostCenter` tag is defined in sceptre config's `stack_tags`
key and that the value assigned to it is valid.  The valid tag values are passed
in with a `file` arg.
```yaml
-   id: check-stack-tags
    args: [--tag=CostCenter, --file=/path/to/valid_tags.json]
```

__Example 2__: Checks that the `CostCenter` tag is defined in sceptre config's `stack_tags`
key and that the value assigned to it is valid.  The valid tag values are from valid_tags.json
excluding `Marketing` and `Operations`.
```yaml
-   id: check-stack-tags
    args: [--tag=CostCenter, --file=/path/to/valid_tags.json --exclude="Marketing" --exclude="Operations"]
```

## Usage

### Stand Alone
Running scripts:

```shell script
➜ check-stack-names ./config/prod/ec2.yaml
- 'foo_ec2' is an invalid stack name [./config/prod/ec2.yaml]
```
__NOTE__: A stack name can contain only alphanumeric characters (case-sensitive) and hyphens.
It must start with an alphabetic character and can't be longer than 128 characters.
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-console-create-stack-parameters.html

```shell script
➜ check-file-names ./config/prod/ec2-datamine.yaml
- stack name does not match file name [./config/prod/ec2-datamine.yaml]
```

```shell script
➜ check-stack-tags --tag CostCenter ./config/prod/ec2.yaml
- stack_tags is missing CostCenter [./config/prod/veoibd-s3.yaml]
```

```shell script
➜ check-stack-tag-values --tag CostCenter --file cost_centers_codes.json ./config/prod/ec2.yaml
- CostCenter tag is not set in config file ./config/prod/ec2.yaml
```

__Note:__ To get usage info run the commands with the `--help` flag


### Pre-commit hook
The scripts can also be [used as a pre-commit hook](https://pre-commit.com/#2-add-a-pre-commit-configuration),
by including the following in `.pre-commit-config.yaml`:
```
-   repo: https://github.com/sceptre/sceptrelint
    rev: INSERT_VERSION
    hooks:
    -    id: check-file-names
    -    id: check-stack-names
    -    id: check-stack-tags
         args: [--tag=CostCenter]
    -    id: check-stack-tag-values
         args: [--tag=CostCenter, --file=/path/to/valid_tags.json]
```
replacing `INSERT_VERSION` with a version tag or commit SHA-1.


After adding the above to `.pre-commit-config.yaml`, run this hook as follows:
```shell script
➜ pre-commit run --all-files
Stack name linter........................................................Failed
- hook id: check-stack-names
- exit code: 1

- 'foo_ec2' is an invalid stack name [./config/prod/ec2.yaml]
```

### Files processing
By default the pre-commit hooks uses the regex defined by `files:` and `exclude:` in
[.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) to gather the files to process.
That configuration setting can be overriden in the local project's
`.pre-commit-config.yaml`.

Override Example:
```yaml
-    id: check-stack-names
     files: ^config/.*(.yaml)$
     exclude: ^config/test/.*$
```

# Aknowledgments
This pre-commit hook is a refactor of the
[pre-commit-provisioner](https://github.com/Sage-Bionetworks-IT/pre-commit-provisioner)
originally created by [Conner Boyle](https://github.com/cascadianblue)
