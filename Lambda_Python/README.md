## Utilização

O script usa os seguintes serviços da AWS:
- CloudWatch
- RDS
- Performance Insights

Este script é executado como uma função Lambda. É necessário fornecer as permissões necessárias para acessar os serviços da AWS mencionados acima.


## Funcionamento

O código inicia-se acessando as instâncias RDS ativas e verificando se elas têm o PI habilitado.

Em seguida, as métricas são coletadas para cada instância habilitada usando a função get_resource_metrics.

As métricas coletadas são enviadas para o CloudWatch usando a função send_cloudwatch_data.
O script pega as instâncias RDS que estão com o Performance Insights habilitado e obtém métricas específicas de desempenho para cada instância. Em seguida, os dados de métricas são enviados para o CloudWatch.


## Variáveis e Funções Importantes

`pi_client`: é o cliente do Performance Insights (PI).

`rds_client`: é o cliente do RDS.

`cw_client`: é o cliente do CloudWatch.

`engine_metrics`: é um dicionário que contém as métricas a serem coletadas para cada tipo de motor (`aurora`, `aurora-postgresql` `aurora-mysql`, `mysql`, `postgresql`).

`get_pi_instances`: retorna uma lista de instâncias RDS com o PI habilitado.

`get_resource_metrics`: coleta as métricas para uma instância específica.

`send_cloudwatch_data`: envia as métricas coletadas para o CloudWatch.