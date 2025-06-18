# AWS App Runner Deployment Guide

This guide will help you deploy the Developer Efficiency Tracker to AWS App Runner with S3 storage using **source code deployment**.

> **Note**: This deployment uses App Runner's source code method with `apprunner.yaml`. No Docker knowledge or container images are required.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Git repository** with your application code
4. **S3 Bucket** for data storage

## Deployment Method: Source Code Repository

We use App Runner's **source code deployment** which:
- ✅ Automatically builds containers from your source code
- ✅ Uses the `apprunner.yaml` configuration file
- ✅ No Dockerfile or container management needed
- ✅ Automatic deployments when you push code changes

Alternative methods (not used in this guide):
- Container Image Repository: Requires building and managing Docker images

## Step 1: Create S3 Bucket

```bash
# Create S3 bucket (replace YOUR_BUCKET_NAME with a unique name)
aws s3 mb s3://YOUR_BUCKET_NAME --region us-east-1

# Enable versioning (recommended)
aws s3api put-bucket-versioning \
    --bucket YOUR_BUCKET_NAME \
    --versioning-configuration Status=Enabled
```

## Step 2: Create IAM Role for App Runner

Create an IAM role with S3 access:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET_NAME",
                "arn:aws:s3:::YOUR_BUCKET_NAME/*"
            ]
        }
    ]
}
```

## Step 3: Configure Environment Variables

Set these environment variables in App Runner:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `USE_S3` | Yes | Enable S3 storage (set to 'true' for production) | `true` |
| `AWS_S3_BUCKET` | Yes | S3 bucket name for data storage | `my-efficiency-tracker-data` |
| `AWS_REGION` | Yes | AWS region where S3 bucket is located | `us-east-1` |
| `BASE_URL` | Yes | Application base URL (App Runner provides this) | `https://abc123.us-east-1.awsapprunner.com` |
| `PORT` | No | Application port (App Runner sets this automatically) | `8080` |
| `ADMIN_PASSWORD` | Recommended | Password for admin access (default: 'admin123') | `your-secure-password` |

## Step 4: Deploy to App Runner

### Option A: Using AWS Console

1. **Open AWS App Runner Console**
   - Go to AWS Console → App Runner

2. **Create Service**
   - Click "Create service"
   - Choose "Source code repository"

3. **Configure Source**
   - Connect to your Git repository
   - Select branch (usually `main` or `master`)
   - Choose "Automatic deployments" for CI/CD

4. **Configure Build**
   - The provided `apprunner.yaml` file handles all build configuration automatically
   - App Runner will:
     - Install Python 3.11 runtime
     - Run `pip install -r requirements.txt`
     - Start the application with `streamlit run app.py --server.port=8080 --server.headless=true`
   - No manual build configuration needed

5. **Configure Service**
   - Service name: `efficiency-tracker`
   - Port: `8080` (automatically configured via `apprunner.yaml`)
   - Environment variables: (see table above)

6. **Configure IAM Role**
   - Create or select IAM role with S3 permissions

7. **Deploy**
   - Review settings and click "Create & deploy"

### Option B: Using AWS CLI

```bash
# Create service using source code repository
aws apprunner create-service \
    --service-name efficiency-tracker \
    --source-configuration '{
        "CodeRepository": {
            "RepositoryUrl": "https://github.com/YOUR_USERNAME/efficiency-tracker",
            "SourceCodeVersion": {
                "Type": "BRANCH",
                "Value": "main"
            },
            "CodeConfiguration": {
                "ConfigurationSource": "CONFIGURATION_FILE",
                "CodeConfigurationValues": {
                    "Runtime": "PYTHON_3",
                    "BuildCommand": "pip install -r requirements.txt",
                    "StartCommand": "streamlit run app.py --server.port=8080 --server.headless=true",
                    "RuntimeEnvironmentVariables": {
                        "USE_S3": "true",
                        "AWS_S3_BUCKET": "YOUR_BUCKET_NAME",
                        "AWS_REGION": "us-east-1",
                        "PORT": "8080",
                        "ADMIN_PASSWORD": "your-secure-password"
                    }
                }
            }
        },
        "AutoDeploymentsEnabled": true
    }' \
    --instance-configuration '{
        "Cpu": "0.25 vCPU",
        "Memory": "0.5 GB",
        "InstanceRoleArn": "arn:aws:iam::ACCOUNT:role/AppRunnerInstanceRole"
    }'
```

> **Note**: Replace `YOUR_USERNAME/efficiency-tracker` with your actual GitHub repository URL.

## Step 5: Post-Deployment Configuration

1. **Update BASE_URL Environment Variable**
   - After deployment, update the `BASE_URL` environment variable with your actual App Runner URL

2. **Test the Application**
   - Access your App Runner URL
   - Test admin interface and engineer interface
   - Verify S3 data persistence

3. **Set up Monitoring** (Optional)
   - Enable CloudWatch logs
   - Set up CloudWatch alarms for health checks

## Step 6: Security Considerations

1. **IAM Permissions**
   - Use least privilege principle
   - Restrict S3 access to specific bucket only

2. **Network Security**
   - App Runner services are publicly accessible by default
   - Consider using VPC connectors for private resources

3. **Data Security**
   - Enable S3 bucket encryption
   - Consider using S3 bucket policies for additional security

## Monitoring and Maintenance

### CloudWatch Logs
App Runner automatically sends logs to CloudWatch. Monitor:
- Application logs
- Health check logs
- Error rates

### Health Checks
The application includes a health check endpoint at `/_stcore/health`

### Scaling
App Runner automatically scales based on traffic:
- Min instances: 1
- Max instances: 25 (default)
- Concurrent requests per instance: 100 (default)

## Troubleshooting

### Common Issues

1. **S3 Permission Errors**
   ```
   Error: Access Denied
   ```
   - Check IAM role permissions
   - Verify bucket name and region

2. **Port Configuration Issues**
   ```
   Error: Connection refused
   ```
   - Ensure PORT environment variable is set to 8080
   - Check Streamlit configuration in Dockerfile

3. **Memory Issues**
   ```
   Error: Container killed due to memory
   ```
   - Increase instance memory configuration
   - Optimize pandas operations

### Debug Commands

```bash
# Check App Runner service status
aws apprunner describe-service --service-arn YOUR_SERVICE_ARN

# View recent logs
aws logs tail /aws/apprunner/efficiency-tracker --follow

# Test S3 connectivity
aws s3 ls s3://YOUR_BUCKET_NAME
```

## Cost Optimization

1. **Right-size Instances**
   - Start with 0.25 vCPU / 0.5 GB memory
   - Monitor and adjust based on usage

2. **S3 Storage Class**
   - Use Standard for active data
   - Consider Standard-IA for archival data

3. **Auto-scaling**
   - Configure appropriate min/max instances
   - Monitor concurrent request patterns

## Support

For issues specific to this application:
1. Check CloudWatch logs
2. Verify environment variables
3. Test S3 connectivity
4. Review IAM permissions

For AWS App Runner issues:
- AWS Documentation: https://docs.aws.amazon.com/apprunner/
- AWS Support: Create a support case 