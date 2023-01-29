import time
import boto3

pi_client = boto3.client('pi')
rds_client = boto3.client('rds')
cw_client = boto3.client('cloudwatch')

engine_metrics = {
    'aurora-mysql': ['os.general.numVCPUs.avg'], #Metricas de S.O
    'aurora-mysql': ['db.Users.Connections.avg'], #Metricas de Banco
    'aurora-mysql': ['db.Locks.innodb_row_lock_waits.avg'] #Metricas não nativas
}


def lambda_handler(event, context):
    pi_instances = get_pi_instances()

    for instance in pi_instances:
        pi_response = get_resource_metrics(instance)
        if pi_response:
            send_cloudwatch_data(pi_response)

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def get_pi_instances():
    response = rds_client.describe_db_instances()

    return filter(
        lambda _: _.get('PerformanceInsightsEnabled', False),   
        response['DBInstances']
    )


def get_resource_metrics(instance):
    metric_queries = []
    if engine_metrics.get(instance['Engine'], False):
        for metric in engine_metrics[instance['Engine']]:
            metric_queries.append({'Metric': metric})

    if not metric_queries:
        return

    return pi_client.get_resource_metrics(
        ServiceType='RDS',
        Identifier=instance['DbiResourceId'],
        StartTime=time.time() - 300,
        EndTime=time.time(),
        PeriodInSeconds=60,
        MetricQueries=metric_queries
    )

def send_cloudwatch_data(pi_response):
    metric_data = []

    for metric_response in pi_response['MetricList']:
        cur_key = metric_response['Key']['Metric']

        for datapoint in metric_response['DataPoints']:
            value = datapoint.get('Value', None)

            if value:
                metric_data.append({
                    'MetricName': cur_key,
                    'Dimensions': [
                        {
                            'Name':'DbiResourceId',    
                            'Value':pi_response['Identifier']
                        } 
                    ],
                    'Timestamp': datapoint['Timestamp'],
                    'Value': datapoint['Value']
                })

    if metric_data:
        cw_client.put_metric_data(
            Namespace='PerformanceInsights',
            MetricData= metric_data
        )