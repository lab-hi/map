curl -X POST \
    -H 'Content-Type: application/json' \
    https://database-1-instance-1.c12lj2a9fkxe.us-east-1.neptune.amazonaws.com:8182/loader -d '
    {
      "source" : "s3://nep-s3-nakamura/geospecies.rdf.gz", 
      "format" : "rdfxml",
      "iamRoleArn" : "arn:aws:iam::527054266437:role/NeptuneLoadFromS3",
      "region" : "us-east-1",
      "failOnError" : "FALSE",
      "parallelism" : "HIGH"
    }'