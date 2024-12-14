import boto3

s3_client = boto3.client(
    's3',
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

bucket_name = "test-bucket"
s3_client.create_bucket(Bucket=bucket_name)

for i in range(100):  # Simulate 100 files
    file_content = f"Sample content for file {i}"
    s3_client.put_object(Bucket=bucket_name, Key=f"file_{i}.txt", Body=file_content)
    print(f"Uploaded file_{i}.txt")

