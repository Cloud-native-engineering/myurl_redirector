# MyURL Redirector

This document describes the MyURL service redirector. Its primary function is to redirect users based on short_codes.

The service comprises two Lambda functions:

## Redirector

The Redirector is publicly accessible and performs redirections based on entries in a DynamoDB table. It also serves as the endpoint for verifying URLs. If a URL is verified, the user is redirected immediately; otherwise, an information page is displayed.

The source code for the Redirector can be found in the `redirector` folder.

## Redirector Data Handler

The Redirector Data Handler ensures that the DynamoDB table contents remain current. It receives updates via an SQS Queue.

The source code for the Redirector Data Handler can be found in the `datahandler` folder.

## Getting Started

Follow these steps to set up the MyURL Redirector service:

1. **Create two AWS Lambda functions:**
    - One function will have an SQS trigger (Redirector Data Handler).
    - The other function will have an Application Gateway (Redirector).

2. **Upload the code to the Lambda functions:**
    - Upload the code from the `redirector` folder to the Redirector function.
    - Upload the code from the `datahandler` folder to the Redirector Data Handler function.

3. **Provision the necessary resources:**
    - Set up an Amazon DynamoDB table to store the URL redirection data.
    - Set up an Amazon SQS Queue to handle updates to the DynamoDB table.

4. **Set up the necessary IAM roles:**
    - The Redirector function needs access to the DynamoDB table for reading data.
    - The Redirector Data Handler function needs access to both the DynamoDB table (for writing data) and the SQS Queue (for receiving updates).

Remember to replace any placeholders in the code with your specific AWS resource names and ARNs.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for details.

## Author Information

This code was created in 2024 by [Yves Wetter](mailto:yves.wetter@edu.tbz.ch).
