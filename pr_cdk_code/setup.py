import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="pr_cdk_code",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "pr_cdk_code"},
    packages=setuptools.find_packages(where="pr_cdk_code"),

    install_requires=[
        "aws-cdk.core==1.56.0",  # 1.56.0
        "aws-cdk.aws-s3",
        "aws-cdk.aws-ssm",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-kms",
        "aws-cdk.aws-iam",
        "aws-cdk.aws-secretsmanager",
        "aws-cdk.aws-elasticsearch",
        "aws-cdk.aws-cognito",
        "aws-cdk.aws-apigateway",
        "aws-cdk.aws-lambda",
        "aws-cdk.aws-sns",
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-wafv2",
        "aws-cdk.aws-route53",
        "aws-cdk.aws-route53-targets",
        "aws-cdk.aws-cloudtrail",
        "aws-cdk.aws-rds",
        "aws-cdk.aws-elasticache",
        "aws-cdk.aws-codepipeline",
        "aws-cdk.aws-codepipeline-actions",

        # Lambda Related imports
        "boto3",
        "botocore",
        "pymysql"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
