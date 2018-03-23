#!/usr/bin/python
import boto3
from datetime import datetime, timedelta

now = datetime.now()
one_day_ago = now - timedelta(hours = 24)

lambda_client = boto3.client('lambda')
cloudwatch_client = boto3.client('cloudwatch')

functions = [ function["FunctionName"] for function in lambda_client.list_functions()["Functions"] ]

for function in functions:
    stats = cloudwatch_client.get_metric_statistics(Namespace="AWS/Lambda", MetricName="Errors",
            Dimensions = [ { "Name" : "FunctionName", "Value" : function } ],
            Statistics = ["Sum"],
            StartTime = one_day_ago, EndTime = now, Period = 60 * 60 * 24)

    errors = 0
    for datapoint in stats["Datapoints"]:
        errors += datapoint["Sum"]
    print("{}\t{}".format(function, errors))
