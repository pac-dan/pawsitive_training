"""
Example environment variables for Pawsitive Training project.
"""

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgres://username:password@localhost:5432/dbname

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=eu-north-1

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET_PAYMENTS=whsec_your_webhook_secret_here
STRIPE_WEBHOOK_SECRET_SUBSCRIPTIONS=whsec_your_webhook_secret_here
STRIPE_PRICE_ID_MONTHLY=price_your_monthly_price_id
STRIPE_PRICE_ID_YEARLY=price_your_yearly_price_id

# Email Configuration (Production only, DEBUG uses console backend)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@pawsitive-training.com

