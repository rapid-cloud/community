__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "MIT"
__email__ = "iroyzis@kinect-consulting.com"

import json
from commands.kc_metadata_manager import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create(self, metadata=None):
        # delete existing aws_infra items
        AwsInfra(self.args).delete_aws_infra("lambda", self.args.name)

        name = self.args.name

        params = {
            "runtime": lambda_runtime,
            "env_vars": {'PROFILE': self.get_env()},
            "timeout": 900,
            "immutable": "false"
        }

        if self.args.lambda_runtime:
            lambda_runtime = self.args.lambda_runtime
        else:
            lambda_runtime = self.get_property('lambda_runtime')

        if self.args.lambda_env_vars:
            params['env_vars'].update(json.loads(self.args.lambda_env_vars))

        if self.args.lambda_memory_size:
            params['memory_size'] = self.args.lambda_memory_size

        if self.args.lambda_timeout:
            params['timeout'] = self.args.lambda_timeout

        if self.args.lambda_schedule:
            params['schedule'] = self.args.lambda_schedule

        params['source_path'] = "default_lambda_template"
        params['immutable'] = True

        super().add_aws_resource('lambda_function', name, params)

        # create CloudWatch Event rule
        if self.args.lambda_schedule:
            # 0 0/15 9-15 ? * MON,TUE,WED,THU,FRI *
            # 5 4 * * ? *
            params ={
                'schedule': self.args.lambda_schedule,
                'target_type': 'lambda_function',
                'target': name,
                'input': {
                    'task_type': self.args.phase
                },       
            }
            super().add_aws_resource('cloudwatch_event_rule', name, params)
