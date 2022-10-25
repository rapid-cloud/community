## RapidCloud Custom Modules

### What is a RapidCloud Module

Module is a set of features to support specific type of AWS resource or set of resources, any business logic as well as convenient and secure way to manage application configurations. For example, `ec2` module suports various features associated with creating and changing EC2 instances. `transform` module accelerates creation of transformation Glue jobs. `trendmicro` module supports integration with Trend Micro Cloud One security products via API.

RapidCloud Modules are used by:

- **Solution Architects** - define and configure solution architecture
- **Automation Engineers** - manage end-to-end infrastructure automation
- **Data Engineers** - create data pipelines and analytics solutions
- **Application Engineers** - develop modular business logic
- **QA Engineers** - create test automation.

RapidCloud Custom Modules are **portable**. A module can be **shared** within and between organizations.

Module can have multiple commands. For example, `ec2` module has following commands:

* `kc ec2 create` to create new EC2 instance
* `kc ec2 list` to list all EC2 modules for current RapidCloud environment
* `kc ec2 enable_trend` to start protecting EC2 instances via Trend Micro Workload Security
*
A module has built-in **CLI** as well as an optional **Console UI**.

RapidCloud has an extensive set of out-of-the-box modules that you can start using right away. We're constantly adding more modules as we determine the on-going demand from RapidCloud users like yourself. [Please let us know](https://www.kinect-consulting.com/contact-us/) what features you'd like to see provided by RapidCloud in the future.

In the meantime, if you require specific functionality that is not supported by RapidCloud, you can develop your own custom modules for RapidCloud by following a few steps outlined below.

<br/>

<a name="start"></a>

### Create new RapidCloud module

* `kc module create` (provide module name and first command via prompts) 

* This creates following custom module skeleton:
    
    * ./commands/modules/<module-name>
        * module.json
        * __init__py
        * console/
            * template_module_{module-name}_{command-name}.json
            * template_module_{module-name}_{command-name}.md

<br/>

### Add new command to your existing custom RapidCloud module

* `kc module add_command` (provide module name and command name via prompts)

* This updates your `module.json`, `__init__.py` and creates console template to include new command skeleton.


<br/>

<a name="customize"></a>

### How to customize your commands

`module.json` drives RapidCloud module functionality.

Here is RapidCloud `rds` module to illustrate configuration sections
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
{
  "rds": {
    "create": {
      "enabled": true,
      "help": "Create RDS or Aurora Database",
      "template_section": "databases",
      "template_enabled": true,
      "create_aws_infra": true,
      "metadata_table": "metadata",
      "id": "name",
      "args": {
        "name": {
          "name": "Name",
          "prompt": "Enter Name with no spaces",
          "required": true,
          "default": ""
        },
        "type": {
          "name": "type",
          "prompt": "Target Database Type (rds|aurora)",
          "required": true,
          "default": "rds"
        },
        "engine": {
          "name": "engine",
          "prompt": "Target Database Engine (mysql|postgres)",
          "required": true,
          "default": "postgres"
        },
        "multi_az": {
          "name": "multi_az",
          "prompt": "Create Target Database in two Availability Zones",
          "required": true,
          "default": "false"
        },
        "database_name": {
          "name": "database_name",
          "prompt": "Target Database Schema Name",
          "required": true,
          "default": "main"
        }
      }
    },
    "add_table": {
      "enabled": true,
      "help": "Add RDS or Aurora Table to an existing database",
      "template_section": "databases",
      "template_enabled": true,
      "create_aws_infra": true,
      "id": "name",
      "args": {
        "name": {
          "name": "Database Table Name",
          "prompt": "Enter Name with no spaces or special characters",
          "required": true,
          "default": ""
        },
        "db_name": {
          "name": "Database Name",
          "prompt": "Enter Existing Database Name",
          "required": true,
          "default": ""
        },
        "primary_key": {
          "name": "Primary Key",
          "prompt": "Enter Table Primary Key",
          "required": true,
          "default": ""
        }
      }
    }
  }
}
```
  </p>
</details>

As you can see, `rds` module has two commands: 

- `kc rds create`
- `kc rds add_table`

A command can have arguments, which are specified in `args` element. When you run a command, CLI will prompt you for every argument in `args`. Argument can be `required` or optional. You can also set `default` value for the argument. 

If you don't want to store an argument in plain text, you can set `type` as `secret` and RapidCloud will automatically store that argument in Secrets Manager.

Example:
```
"some_api_key": {
  "name": "some_api_key",
  "type": "secret",
  "prompt": "Some confidential API Key (saved in Secretes Manager)",
  "required": true,
  "default": ""
}
```

Once all the arguments are collected, RapidCloud will call a Python function in `__init__.py`, with the same name as the command. So if you run `kc rds create`, it will call `create` function in your module's `__init__.py`. All provided arguments will be automatically saved in `metadata` DynamoDB table in your environment account. The rest of functionality will be added by you in the `__init__.py` `create` function, which includes in-code instructions for your convenience. 

Here is a template function code that is generated when you create a module
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
def create(self, metadata=None):
    # Step 1
    '''
    Delete existing `aws_infra` items.
    Module automation metadata is stored in your DynamoDB `aws_infra` table
    delete existing aws_infra items for your module instance
    '''
    AwsInfra(self.args).delete_aws_infra(self.args.module, self.args.name)

    # Step 2
    '''
    Construct `params` dict for each AWS resource you plan to create for this module.
    Params will be used by terraform modules to generate your infrastructure
    '''
    # example:
    params = {
        "resource_name": "some_name",
        "category": "testing",
        "size": 5
    }

    # Step 3
    '''
    Create `aws_infra` item for each AWS resource you plan to automate
    '''
    # example:

    # must be a valid Terraform supported AWS resource type
    resource_type = "lambda_function"

    # must be a unique resource name for the specified resource_type
    resource_name = "some_name"
    # TODO uncomment if needed
    # super().add_aws_resource(resource_type, resource_name, params)

    # TODO
    '''
    Repeat steps 2 and 3 for each resource to be generated for this module
    '''

    # TODO
    '''
    Optionally and in addition to creating resources, you can run any code here 
    to support this module functionality.

    For example, enable or disable CloudWatch event rules, send SNS or SES message, 
    upload or download files to/from S3, update database records, kick-off 
    DMS jobs, start Glue workflows, etc
    '''
```
  </p>
</details>


<br/>

<a name="terraform"></a>

### How to add custom terraform templates and modules

RapidCloud uses Terraform for infrastructure automation. Each AWS resource type supported by RapidCloud has a jinja template and an optional terraform module code. If you want to add custom terraform automation features to your RapidCloud module, follow these simple steps:

1. Create jinja template for the resource not currently supported by RapidCloud and save it in `./terraform/custom_templates` directory. Jinja template must have following naming convention: `{resource_type}.j2`, where `{resource_type}` is the AWS resource type supported by terraform. For example, `lambda_function.j2`, `aws_instance.j2`, etc

2. For simple resources, your jinja template will provide all the functionality to generate final terraform code. For more complex resources you'll need to create corresponding terraform module code, and save in `./terraform/modules` directory. Terraform module code must be placed in its own directory `{resource_type}`, where `{resource_type}` is the AWS resource type supported by terraform. For example, `lambda_function`, `aws_instance`, etc. See currently supported RapidCloud modules in your `./terraform/modules`.

<br/>

Here is an example of jinja template to support `sns_topic_subscription` automation. This is a simple resource, therefore there is no corresponding *.tf code.

#### Jinja Template - ./terraform/custom_templates/sns_topic_subscription.j2

<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
resource "aws_lambda_permission" "{{ profile }}-{{ resource_type }}-{{ resource_name }}" {
  action        = "lambda:InvokeFunction"
  function_name  = module.{{ profile }}_{{ params['function_name'] }}_lambda_function.name
  principal     = "sns.amazonaws.com"
  statement_id  = "AllowSubscriptionToSNS"
  source_arn    = aws_sns_topic.{{ profile }}-sns_topic-{{ params['topic_name'] }}.arn
}

resource "aws_sns_topic_subscription" "{{ profile }}-{{ resource_type }}-{{ resource_name }}" {
  endpoint  = module.{{ profile }}_{{ params['function_name'] }}_lambda_function.arn
  protocol  = "lambda"
  topic_arn = aws_sns_topic.{{ profile }}-sns_topic-{{ params['topic_name'] }}.arn
}
```
  </p>
</details>

<br/>

Here is an example of a more complex resource, which includes both jinja template and terraform module, to support `s3_bucket` automation.

#### Jinja Template - ./terraform/custom_templates/s3_bucket.j2
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
module "{{ profile }}_{{ resource_name }}_{{ resource_type }}" {
  source        = "../modules/{{ resource_type }}"
  bucket_name   = "${replace("{{ profile }}_{{ resource_name }}", "_", "-")}"
  kms_key_arn   = aws_kms_key.{{ profile }}.id
  tags = {
    Name = "{{ profile }}_{{ resource_name }}"
    "env" = "{{ env }}"
    "profile" = "{{ name }}"
    "workload" = "{{ workload }}"
    "client" = "{{ client }}"
    "author" = "rapid-cloud-by-kinect"
  }
}
```
  </p>
</details>

#### Terraform Module Code - ./terraform/modules/s3_bucket/iam.tf
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
resource "aws_iam_role" "role" {
  count = var.enable_bucket_policy ? 1 : 0
  name  = "${var.bucket_name}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "dms.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach" {
  count      = var.enable_bucket_policy ? 1 : 0
  role       = aws_iam_role.role.0.name
  policy_arn = aws_iam_policy.policy.0.arn
}

data "aws_iam_policy_document" "policy_json" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      aws_s3_bucket.s3.arn,
      "${aws_s3_bucket.s3.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "policy" {
  count  = var.enable_bucket_policy ? 1 : 0
  name   = "dms-datalake-s3-${var.bucket_name}-policy"
  policy = data.aws_iam_policy_document.policy_json.json
}
```
  </p>
</details>

#### Terraform Module Code - ./terraform/modules/s3_bucket/output.tf
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
output "bucket_arn" {
  value = aws_s3_bucket.s3.arn
}

output "bucket_name" {
  value = aws_s3_bucket.s3.id
}
```
  </p>
</details>

#### Terraform Module Code - ./terraform/modules/s3_bucket/s3.tf
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
resource "aws_s3_bucket" "s3" {
  bucket = var.bucket_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = merge(var.tags, map("Name", var.bucket_name))
}

resource "aws_s3_bucket_public_access_block" "s3_public_access" {
  bucket = aws_s3_bucket.s3.id
  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}
```
  </p>
</details>

#### Terraform Module Code - ./terraform/modules/s3_bucket/variables.tf
<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
variable "bucket_name" {
  description = "The name of the s3 bucket to create"
  type        = string
}

variable "tags" {
  description = "Map of tags to assign to this bucket"
  type        = map(string)
}

variable "kms_key_arn" {
  description = "ARN of the kms key used to encrypt the bucket"
  type        = string
}

variable "enable_bucket_policy" {
  description = "Enable bucket policy"
  type        = bool
  default     = true
}

variable "block_public_acls" {
  type    = bool
  default = true
}

variable "block_public_policy" {
  type    = bool
  default = true
}

variable "ignore_public_acls" {
  type    = bool
  default = true
}

variable "restrict_public_buckets" {
  type    = bool
  default = true
}
```
  </p>
</details>


<br/>

### Variables available in your jinja templates

#### {{ client }}

Your orgnization abbreviation. Example `mycrop`

#### {{ workload }}

Your workload/application name. Example `orders`

#### {{ env }}

Your workload/application phase/env. Example `dev`

#### {{ profile }}

Fully qualified name of your environment. Example `mycorp_orders_dev`

#### {{ resource_name }}

Resource name provided in your `__init__.py` code in the following line:

`super().add_aws_resource(resource_type, resource_name, params)`

#### {{ resource_type }}

Resource type provided in your `__init__.py` code in the following line:

`super().add_aws_resource(resource_type, resource_name, params)`

#### {{ params['argument_name_for_your_module'] }}

Argument defined in your `module.json` and collected from CLI or Console. 

<br/>

<a name="console"></a>

### template_module_{module-name}_{command-name}.json

Each module command will have a skeleton console template created by RapidCloud. If you want to use module features in RapidCloud Console UI in addition to the CLI, then you'll need to modify the template. 

Here is an RDS console template for `kc rds create` command. It contains two sections:

1. Grid, showing a list of RDS databases for your environment
2. Form that collects RDS configuration/arguments when adding or editing RDS instance 

<details>
  <summary>
    &gt;&gt; Show code
  </summary>
  <p>
```
{
  "type": "Theia::Action",
  "label": "RDS/Aurora",
  "id": "rds",
  "steps": [
    {
      "type": "Theia::Step::Grid",
      "id": "rds",
      "datasource": "data?type=metadata&filter_name=module&filter_value=rds",
      "env_param_required": true,
      "columns": ["name","rds_engine","rds_type"],
      "title": "Databases",
      "description": "",
      "submit": "Continue"
    },
    {
      "type": "Theia::Step::Form",
      "id": "rds",
      "title": "",
      "description": "",
      "submit": "Submit",
      "commands": [
        {
          "label": "Remove",
          "require_confirmation": true,
          "confirmation_message": "Are you sure you want to remove this item?",
          "command": {
            "phase": "undo-command"
          }
        },
        {
          "label": "Create",
          "command": {
            "phase": "rds",
            "command": "create",
            "refresh_status": true                 
          }
        }
      ],
      "controls": [
        {
          "type": "Theia::Control::Input",
          "id": "name",
          "label": "Database Name",
          "help": "Enter database name (no space or special characters)",
          "inputType": "text"
        },
        {
          "type": "Theia::Control::Select",
          "id": "rds_engine",
          "label": "Database Engine",
          "help": "",
          "options": [
            {
              "type": "Theia::Option",
              "label": "MySQL",
              "value": "mysql"
            },
            {
              "type": "Theia::Option",
              "label": "PostgreSQL",
              "value": "postgres"
            }
          ]
        },
        {
          "type": "Theia::Control::Select",
          "id": "rds_type",
          "label": "AWS Database Service",
          "help": "",
          "options": [
            {
              "type": "Theia::Option",
              "label": "RDS",
              "value": "rds"
            },
            {
              "type": "Theia::Option",
              "label": "Aurora",
              "value": "aurora"
            }
          ]
        },
        {
          "type": "Theia::Control::Select",
          "id": "rds_multi_az",
          "label": "Multi Az",
          "help": "Multi Az",
          "default": "no",
          "options": [
            {
              "type": "Theia::Option",
              "label": "Yes",
              "value": "yes"
            },
            {
              "type": "Theia::Option",
              "label": "No",
              "value": "no"
            }
          ]
        },
        {
          "type": "Theia::Control::Input",
          "id": "rds_database_name",
          "label": "Schema Name",
          "help": "Enter schema name (no space or special characters)",
          "inputType": "text"
        }
      ]
    }
  ]
}
```
  </p>
</details>

#### Here are supported form controls with examples

**Text Input Field**

```
{
  "type": "Theia::Control::Input",
  "id": "name",
  "label": "Database Name",
  "help": "Enter database name (no space or special characters)",
  "inputType": "text"
}
```

**Select (aka Drop Down)**

```
{
  "type": "Theia::Control::Select",
  "id": "rds_type",
  "label": "AWS Database Service",
  "help": "",
  "options": [
    {
      "type": "Theia::Option",
      "label": "RDS",
      "value": "rds"
    },
    {
      "type": "Theia::Option",
      "label": "Aurora",
      "value": "aurora"
    }
  ]
}
```

**Multi-Select**

```
{
    "type": "Theia::Control::MultiSelect",
    "id": "transform_base_datasets",
    "label": "Base Datasets",
    "help": "Select source datasets for this transformation",
    "options": [
      {
        "type": "Theia::Option",
        "label": "Dataset 1",
        "value": "dataset1"
      },
      {
        "type": "Theia::Option",
        "label": "Dataset 2",
        "value": "dataset2"
      },
      {
        "type": "Theia::Option",
        "label": "Dataset 3",
        "value": "dataset3"
      },
      {
        "type": "Theia::Option",
        "label": "Dataset 4",
        "value": "dataset4"
      },
      {
        "type": "Theia::Option",
        "label": "Dataset 5",
        "value": "dataset5"
      }
    ]
}
```

**Toggle**

```
{
  "type": "Theia::Control::Toggle",
  "id": "ecr_scan_on_push",
  "label": "Scan Images on Push"
}
```

**Key/Value**

```
{
  "type": "Theia::Control::KeyValue",
  "id": "lambda_env_vars",
  "label": "Environment Variables",
  "dynamic_datasource": "data?type=metadata&filter_name=module,name&filter_value=lambda,${name}&&result=params,lambda_env_vars",
  "add_value_label": "Add new environment variable for your Lambda Function"
}
```

<br/>

### template_module_{module-name}_{command-name}.md

You can add Help Information to your module to have it displayed in the RapidCloud console. Just add markdown content to the auto-generated `template_module_{module-name}_{command-name}.md` file. Then you'll see an `"i"` icon which when clicked, will show the help section on the right side.

<br/>

<a name="activate_deactivate"></a>

### Activate / Deactivate Custom Modules

Once you're done testing module CLI functionality, you can modify your module console templates as per above and add to the RapidCloud console by running `kc module activate` command.

If you want to remove your module from the console, run `kc module deactivate`

_NOTE_: run `kc module activate` if you want to apply changes to the console template `json` or `md` files. 

<br/>

<a name="export_install"></a>

### Export / Install Custom Modules

RapidCloud Custom Modules can be **shared** within and between organization. 

#### Export Custom module

Run `kc module export --name {custom_module_name} --no-prompt` to create a portable zip file for your custom module.

#### Install Custom Module

Run `kc module install --name {custom_module_name} --module_zipfile_path {full_path_to_custom_module_zipfile}  --no-prompt` to install custom module from module export zip file.

<br/>

### RapidCloud version upgrades

When upgrading to new versions of RapidCloud, your custom modules will not be affected, but we recommend using your source control of choice to keep your custom module code safe, as with any custom code you work on.
