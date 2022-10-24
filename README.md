## RapidCloud Community repo for custom modules

RapidCloud automation and acceleration framework provides an easy way to add custom functionality to your existing RapidCloud distribution.

Modules in this repo are free to use and share with others.

Check out RapidCloud Custom Modules documentation at https://rapid-cloud.io/custom-modules/

Here is a quick start guide:

### Create new RapidCloud module

`kc module create` (provide module name and first command via prompts)

This creates following custom module skeleton:
    
* ./commands/modules/<module-name>
    * module.json
    * __init__py
    * console/
        * template_module_{module-name}_{command-name}.json
        * template_module_{module-name}_{command-name}.md


### Add new command to your existing custom RapidCloud module

`kc module add_command` (provide module name and command name via prompts)

* This updates your `module.json`, `__init__.py` and creates console template to include new command skeleton.


### Customize command arguments

`module.json` drives RapidCloud module functionality


### How to add custom terraform templates and modules

RapidCloud uses Terraform for infrastructure automation. Each AWS resource type supported by RapidCloud has a jinja template and an optional terraform module code. If you want to add custom terraform automation features to your RapidCloud module, follow these simple steps:

1. Create jinja template for the resource not currently supported by RapidCloud and save it in `./terraform/custom_templates` directory. Jinja template must have following naming convention: `{resource_type}.j2`, where `{resource_type}` is the AWS resource type supported by terraform. For example, `lambda_function.j2`, `aws_instance.j2`, etc

2. For simple resources, your jinja template will provide all the functionality to generate final terraform code. For more complex resources you'll need to create corresponding terraform module code, and save in `./terraform/modules` directory. Terraform module code must be placed in its own directory `{resource_type}`, where `{resource_type}` is the AWS resource type supported by terraform. For example, `lambda_function`, `aws_instance`, etc. See currently supported RapidCloud modules in your `./terraform/modules`.


### RapidCloud Module Console pages - template_module_{module-name}_{command-name}.json

Each module command will have a skeleton console template created by RapidCloud. If you want to use module features in RapidCloud Console UI in addition to the CLI, then you'll need to modify the template. 


### RapidCloud Module Console help info - template_module_{module-name}_{command-name}.md

You can add Help Information to your module to have it displayed in the RapidCloud console. Just add markdown content to the auto-generated `template_module_{module-name}_{command-name}.md` file. Then you'll see an `"i"` icon which when clicked, will show the help section on the right side.


### Activate / Deactivate Custom Modules

Once you're done testing module CLI functionality, you can modify your module console templates as per above and add to the RapidCloud console by running `kc module activate` command.

If you want to remove your module from the console, run `kc module deactivate`

_NOTE_: run `kc module activate` if you want to apply changes to the console template `json` or `md` files. 


### Export / Install Custom Modules

RapidCloud Custom Modules can be **shared** within and between organization. 


#### Export Custom module

Run `kc module export --name {custom_module_name} --no-prompt` to create a portable zip file for your custom module.


#### Install Custom Module

Run `kc module install --name {custom_module_name} --module_zipfile_path {full_path_to_custom_module_zipfile}  --no-prompt` to install custom module from module export zip file.


### RapidCloud version upgrades

When upgrading to new versions of RapidCloud, your custom modules will not be affected, but we recommend using your source control of choice to keep your custom module code safe, as with any custom code you work on.

