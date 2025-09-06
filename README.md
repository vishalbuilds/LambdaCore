# AWS Lambda Functions

## List of Functions

1. [Function 1](#function-1)
2. [Function 2](#function-2)
3. [Function 3](#function-3)

## Function Details

### Function 1
Description of Function 1.

### Function 2
Description of Function 2.

### Function 3
Description of Function 3.

### Lambda container local test.



Build lambda container
```
podman build --build-arg lambda_handler_env=lambda_handler.lambda_handler --build-arg build=local -t lambda-core .  
```

Run lambda container
```
podman run -p 9000:8080 lambda-core
```

Test container by sending request
```
curl "http://localhost:9000/2015-03-31/functions/function/invocations"  -d @"src/test_data/StatusChecker/StatusChecker.json"
```